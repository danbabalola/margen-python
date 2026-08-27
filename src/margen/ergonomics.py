"""Notebook-friendly helpers over the generated Margen client.

HAND-WRITTEN, not generated. Preserved across Speakeasy regenerations via the
repo-root .genignore. These wrap the typed SDK to add the things a data-science
workflow wants and a codegen cannot produce: paginated iteration and a one-call
"download my whole selection to a folder".

    from margen import Margen
    from margen.ergonomics import iter_items, iter_lineages, download_selection

    client = Margen(bearer_auth="mgn_test_...")   # your API key from /keys

    picks = list(iter_items(client, benchmark="synthetic-face-v1", kind="fake"))
    saved = download_selection(client, picks, "out/")
"""

from __future__ import annotations

import io
import json
import os
import random
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Dict, Iterator, List, Optional

from margen import Margen, errors, models

__all__ = [
    "iter_items",
    "iter_lineages",
    "iter_distinct_identities",
    "group_by_identity",
    "unique_identities",
    "download_selection",
    "get_release",
    "pull_release",
]

_PAGE_KEYS = ("limit", "offset", "cursor", "lineage", "distinct_identities")


def _normalize_filters(filters: dict) -> dict:
    """Let callers pass a Python list/tuple for any multi-value filter.

    The typed client and the API want multiple values as one comma-separated
    string (form style, e.g. ``skin_tone=dark,brown``), so a list/tuple is
    joined here. A plain string is passed through unchanged, so both
    ``skin_tone="dark"`` and ``skin_tone=["dark", "brown"]`` work.
    """
    out: dict = {}
    for key, value in filters.items():
        if key == "exclude_owned":
            # Convenience: accept a Python bool. The API wants the string "true"
            # (or the param omitted), so True/"true" -> "true", anything falsy is
            # dropped so it is never sent.
            if value is True or value == "true":
                out[key] = "true"
            continue
        if isinstance(value, (list, tuple)):
            out[key] = ",".join(str(v) for v in value)
        else:
            out[key] = value
    return out


def iter_items(client: Margen, *, page_size: int = 500, **filters) -> Iterator[models.AttackDataItem]:
    """Yield every matching item, paging with offset/limit under the hood.

    Filters mirror ``client.list_items`` (benchmark, skin_tone, gender, kind,
    generator, perturbation, layer, source_real_id, ...); a list value is ORed.
    ``page_size`` is capped at 500 server-side.

    Pass ``exclude_owned=True`` to yield only images this account does NOT
    already own, so a re-run (e.g. after topping up credits) skips everything
    already pulled and downloads just the new images. Feed the result straight to
    ``download_selection``.
    """
    for key in _PAGE_KEYS:
        filters.pop(key, None)
    filters = _normalize_filters(filters)
    offset = 0
    while True:
        resp = client.list_items(limit=page_size, offset=offset, **filters)
        page = resp.result if resp is not None else None
        data = (page.data if page is not None else None) or []
        yield from data
        if not data or page is None or not page.has_more:
            break
        offset += len(data)


def iter_lineages(client: Margen, *, page_size: int = 100, **filters) -> Iterator[models.AttackDataItem]:
    """Yield every item of every matched lineage (real + its fakes + perturbed
    variants), paging by lineage. Filters select which lineages match; whole
    lineages are returned.
    """
    for key in _PAGE_KEYS:
        filters.pop(key, None)
    filters = _normalize_filters(filters)
    offset = 0
    while True:
        resp = client.list_items(lineage="true", limit=page_size, offset=offset, **filters)
        page = resp.result if resp is not None else None
        data = (page.data if page is not None else None) or []
        yield from data
        if not data or page is None or not page.has_more:
            break
        # Lineage mode pages by lineage: advance by the distinct lineages returned.
        offset += len({it.source_real_id for it in data if it.source_real_id})


def iter_distinct_identities(
    client: Margen, *, page_size: int = 500, **filters
) -> Iterator[models.AttackDataItem]:
    """Yield ONE representative item per identity (server-side dedupe by person).

    Opt-in server mode (no default cap). Composes with filters, e.g.
    ``iter_distinct_identities(client, benchmark=..., kind="real")`` yields one
    real image per person. The representative is deterministic. Feed straight to
    ``download_selection``.
    """
    for key in _PAGE_KEYS:
        filters.pop(key, None)
    filters = _normalize_filters(filters)
    offset = 0
    while True:
        resp = client.list_items(distinct_identities="true", limit=page_size, offset=offset, **filters)
        page = resp.result if resp is not None else None
        data = (page.data if page is not None else None) or []
        yield from data
        if not data or page is None or not page.has_more:
            break
        offset += len(data)  # one row per identity, so advance by rows returned


def group_by_identity(items) -> Dict[Optional[str], List]:
    """Client-side: group already-pulled items by ``identity_id`` (the reconciled
    person). Items with no identity_id are grouped under ``None``."""
    groups: Dict[Optional[str], List] = {}
    for it in items:
        groups.setdefault(getattr(it, "identity_id", None), []).append(it)
    return groups


def unique_identities(items, *, n: int = 1, seed: Optional[int] = None) -> List:
    """Client-side: keep at most ``n`` item(s) per identity from an already-pulled
    list (dedupe / cap by person). Deterministic (keeps input order) unless a
    ``seed`` is given, which shuffles within each identity reproducibly. Items with
    no identity_id can't be deduped, so each is kept."""
    out: List = []
    for key, members in group_by_identity(items).items():
        if key is None:
            out.extend(members)
            continue
        picks = list(members)
        if seed is not None:
            random.Random(seed).shuffle(picks)
        out.extend(picks[:n])
    return out


def download_selection(
    client: Margen,
    items,
    out_dir: str,
    *,
    progress: bool = True,
    run_id: Optional[str] = None,
) -> List[str]:
    """Download a selection of items to ``out_dir``. ``items`` is an iterable of
    item objects (from :func:`iter_items`) or bare item-id strings.

    - Two-step per item: ``download_item`` returns a signed URL, then the bytes
      are fetched with a plain HTTP request (no auth header), within the URL TTL.
    - Live tier debits one credit per item; test tier is free.
    - The Idempotency-Key is deterministic per item within this run, so a retry
      of the same item is a no-op (no double charge); a fresh run charges again.
    - Preflights ``get_usage`` and warns if the balance cannot cover the selection.
    - On 402 (out of credits) it STOPS and reports how many were saved.

    Returns the list of saved file paths.
    """
    items = list(items)
    os.makedirs(out_dir, exist_ok=True)
    run_id = run_id or str(uuid.uuid4())
    total = len(items)

    try:
        usage = client.get_usage()
        if getattr(usage, "tier", None) != "test":
            balance = getattr(usage, "balance", None)
            if isinstance(balance, int) and balance < total:
                print(f"[warn] credit balance {balance} < {total} requested; will stop when exhausted", flush=True)
    except errors.MargenError:
        pass  # preflight is best-effort

    saved: List[str] = []
    for i, item in enumerate(items, 1):
        item_id = _item_id(item)
        try:
            dl = client.download_item(item_id=item_id, idempotency_key=f"{run_id}:{item_id}")
        except errors.MargenError as exc:
            if getattr(exc, "status_code", None) == 402:
                print(f"[stop] out of credits after {len(saved)}/{total} saved", flush=True)
                break
            print(f"[skip] {item_id}: {exc}", flush=True)
            continue
        if not getattr(dl, "url", None):
            continue
        dest = os.path.join(out_dir, _filename(getattr(dl, "item", None), item_id))
        _fetch(dl.url, dest)
        saved.append(dest)
        if progress:
            balance = getattr(dl, "balance", None)
            if getattr(dl, "already_owned", False):
                # Own-once: a re-download of an image this account already paid
                # for. No credit is taken, so make that explicit rather than
                # printing an unchanged balance that looks like a silent charge.
                suffix = " (already owned, no charge)"
            elif balance is not None:
                suffix = f" balance={balance}"
            else:
                suffix = " (free)"
            print(f"[{i}/{total}] {os.path.basename(dest)}{suffix}", flush=True)
    return saved


def get_release(client: Margen, *, benchmark: str) -> dict:
    """Fetch the bulk release for a benchmark: signed URLs for every shard set the
    key can access, plus the credit cost. Does not download anything.

    The bulk endpoint is newer than the generated client, so this calls it through
    the client's configured base URL and bearer token. Raises ``RuntimeError`` on
    an insufficient-credit (402) response, with the server's message.

    ``benchmark`` is a benchmark id, e.g. ``"passport-pad-v1"`` or
    ``"synthetic-face-v1"``. The request is identical for either; the response's
    ``coverage`` field tells you what your key was entitled to.
    """
    base = client.sdk_configuration.get_server_details()[0]
    url = f"{base}/api/v1/data/release?benchmark={urllib.parse.quote(benchmark)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {_bearer(client)}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body = {}
        try:
            body = json.loads(exc.read())
        except Exception:  # pragma: no cover - non-JSON error body
            pass
        raise RuntimeError(body.get("error") or f"release request failed: HTTP {exc.code}") from None


def pull_release(client: Margen, *, benchmark: str, out_dir: Optional[str] = None):
    """Download a whole benchmark as prebuilt parquet shards and return one pandas
    DataFrame. This is the copy-paste bulk entry point.

    - One credit per image, net of images you already own; a re-pull is free.
    - If your access does not line up with whole shard sets (``coverage`` is
      ``"partial"`` or ``"empty"``), there is nothing to bulk-download: this raises
      ``RuntimeError`` telling you to use per-image :func:`download_selection`.
    - ``out_dir`` optionally also saves the ``.parquet`` files to a folder.

    Needs ``pandas`` (with a parquet engine such as ``pyarrow``).
    """
    try:
        import pandas as pd  # local import: the SDK does not depend on pandas
    except ImportError:  # pragma: no cover
        raise RuntimeError("pull_release needs pandas: pip install 'margen[data]' or pip install pandas pyarrow") from None

    release = get_release(client, benchmark=benchmark)
    shards = release.get("shards") or []
    if not shards:
        raise RuntimeError(
            f"coverage={release.get('coverage')}: your access does not cover a whole "
            "shard set, so there is nothing to bulk-download. Use download_selection "
            "for per-image access."
        )
    print(f"{release.get('credits_required')} credits, {len(shards)} sets", flush=True)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    frames = []
    for shard in shards:
        for part in shard.get("parts", []):
            with urllib.request.urlopen(part["url"], timeout=300) as resp:
                blob = resp.read()
            if out_dir:
                with open(os.path.join(out_dir, f"{shard['set']}-{part['part']:03d}.parquet"), "wb") as fh:
                    fh.write(blob)
            frames.append(pd.read_parquet(io.BytesIO(blob)))
    return pd.concat(frames, ignore_index=True)


def _bearer(client: Margen) -> str:
    sec = client.sdk_configuration.security
    if callable(sec):
        sec = sec()
    token = getattr(sec, "bearer_auth", None) if sec is not None else None
    if not token:
        raise RuntimeError("no API key on the client: Margen(bearer_auth='mgn_...')")
    return token


# --- helpers -----------------------------------------------------------------

def _item_id(item) -> str:
    if hasattr(item, "id"):
        return item.id
    if isinstance(item, dict):
        return item["id"]
    return str(item)


def _val(value) -> Optional[str]:
    value = getattr(value, "value", value)  # enum -> its value
    return str(value) if value is not None else None


def _filename(item, item_id: str) -> str:
    st = _val(getattr(item, "skin_tone", None)) or "na"
    gn = _val(getattr(item, "gender", None)) or "na"
    kd = _val(getattr(item, "kind", None)) or "na"
    pt = _val(getattr(item, "perturbation", None)) or "clean"
    return f"{st}_{gn}_{kd}_{pt}_{str(item_id)[:8]}.jpg"


def _fetch(url: str, dest: str) -> int:
    with urllib.request.urlopen(url, timeout=300) as resp, open(dest, "wb") as fh:
        total = 0
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            fh.write(chunk)
            total += len(chunk)
    return total

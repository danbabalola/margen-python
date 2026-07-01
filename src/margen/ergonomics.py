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

import os
import urllib.request
import uuid
from typing import Iterator, List, Optional

from margen import Margen, errors, models

__all__ = ["iter_items", "iter_lineages", "download_selection"]

_PAGE_KEYS = ("limit", "offset", "cursor", "lineage")


def iter_items(client: Margen, *, page_size: int = 500, **filters) -> Iterator[models.AttackDataItem]:
    """Yield every matching item, paging with offset/limit under the hood.

    Filters mirror ``client.list_items`` (benchmark, skin_tone, gender, kind,
    generator, perturbation, layer, source_real_id, ...); a list value is ORed.
    ``page_size`` is capped at 500 server-side.
    """
    for key in _PAGE_KEYS:
        filters.pop(key, None)
    offset = 0
    while True:
        resp = client.list_items(limit=page_size, offset=offset, **filters)
        page = resp.result if resp is not None else None
        data = (page.data if page is not None else None) or []
        for item in data:
            yield item
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
    offset = 0
    while True:
        resp = client.list_items(lineage="true", limit=page_size, offset=offset, **filters)
        page = resp.result if resp is not None else None
        data = (page.data if page is not None else None) or []
        for item in data:
            yield item
        if not data or page is None or not page.has_more:
            break
        # Lineage mode pages by lineage: advance by the distinct lineages returned.
        offset += len({it.source_real_id for it in data if it.source_real_id})


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
            suffix = f" balance={balance}" if balance is not None else " (free)"
            print(f"[{i}/{total}] {os.path.basename(dest)}{suffix}", flush=True)
    return saved


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

# Changelog

All notable changes to the `margen` Python SDK. Versioning follows SemVer; the
SDK version is decoupled from the API version. See the API's own versioning
policy for the wire contract.

## [0.1.9]

### Added
- `identity_id` on `AttackDataItem`: the reconciled PERSON identity (spans all of a person's source images/videos; a real and its identity-preserving fakes share it). Broader than `source_real_id` (one source image's lineage). Additive wire field; requires a `speakeasy run` regenerate to appear typed on the model.
- Opt-in server dedupe: `distinct_identities="true"` on `list_items` returns ONE representative item per identity (composes with filters, e.g. `kind="real"` -> one real per person; no default cap). New ergonomic iterator `iter_distinct_identities(client, **filters)`.
- Client-side helpers `unique_identities(items, n=1, seed=None)` (cap/dedupe an already-pulled list by person) and `group_by_identity(items)` (`{identity_id: [items]}`). Gating is left to the user by design; no default identity cap.

## [0.1.8]

### Changed
- Lowered the minimum Python from 3.10 to 3.9 (`requires-python = ">=3.9"`), so `pip install margen` works on 3.9. The generated client is typing-based (no `match`, no PEP 604 runtime unions) and the dependencies (pydantic 2.11, httpx 0.28) support 3.9; 3.9 is the true floor, pydantic 2.11 itself requires it. NOTE: a future `speakeasy run` may reset this to the generator default (3.10); re-apply `>=3.9` after regenerating.

## [0.1.7]

### Added
- `iter_items` / `iter_lineages` accept `exclude_owned=True` (as well as the API's `"true"`): yields only images the account does not already own, so a re-run after topping up credits skips everything already pulled and downloads just the new images.

### Changed
- `download_selection` progress now prints `(already owned, no charge)` for own-once re-downloads, instead of an unchanged balance that looked like a silent charge.

## [0.1.6]

### Removed
- `variant_group` (the `list_items` filter and the `AttackDataItem` field, both added in 0.1.5). It does not apply to `synthetic-face-v1`: the backing grouping id is absent and synthetic faces are independent, not grouped variants, so the field was always null. `scene` is unaffected. The concept returns with the variation-based benchmarks (face-swap, puppeteering) where a real grouping exists.

## [0.1.5]

### Added
- `list_items` gains two `synthetic-face-v1` filters: `scene` (indoor | outdoor | selfie; synthetic-only, reals have none) and `variant_group` (opaque generation-cluster id; filter by one value to pull near-duplicate synthetic siblings, or dedup to one per group).
- `AttackDataItem.scene` and `AttackDataItem.variant_group` fields (both null for reals). `variant_group` is navigation/lineage only; it exposes no generation recipe and is not a billing bundle.

## [0.1.4]

### Added
- `list_items` (and `download_item`) now expose `include` (opt-in extras, comma-separated). Pass `include="metadata"` to attach the full per-image label object under each item's `metadata`. Browsing labels is free; only `/download` costs a credit.
- `AttackDataItem.metadata` — the full flat label object, present only when the request passes `include=metadata`.
- `AttackDataItem.base_id` — the base image a variant derives from; hold it and change `perturbation` to pull another condition of the same image. Also a filter on `list_items`.
- `exclude_owned` on `list_items` (offset mode): omit images you already own, with `remaining`/`owned`/`total_matching` and a `subset_exhausted` message.

### Changed
- Regenerated the typed client from the current API spec, which the SDK's vendored spec had drifted behind. `source_dataset` is no longer on the wire.

## [0.1.3]

### Changed
- `iter_items` and `iter_lineages` now accept a Python list or tuple for any multi-value filter (e.g. `skin_tone=["dark", "brown"]`), joining it to the comma-separated form the API expects. A plain string still works unchanged, so both `skin_tone="dark"` and `skin_tone=["dark", "brown"]` are valid. This matches how notebook users naturally express an OR set; previously a list raised a client-side `ValidationError`. The raw typed `client.list_items` still takes the comma-separated string.

## [0.1.2]

### Changed
- Default production server is now `https://www.margensoftware.com`. The apex `margensoftware.com` permanently redirects to `www`, and a cross-host redirect can drop the `Authorization` header, so the SDK now targets the canonical host directly. Upgrade from 0.1.0/0.1.1, or pass `Margen(server_url="https://www.margensoftware.com")`.

## [0.1.1]

### Added
- `margen.ergonomics` hand-written helpers over the typed client:
  - `iter_items(client, **filters)` and `iter_lineages(client, **filters)` — paginate the full result set.
  - `download_selection(client, items, out_dir)` — one-call bulk download to a folder (two-step signed-URL fetch, deterministic per-item idempotency, `/usage` preflight, stop-on-402).
- `notebooks/quickstart.ipynb` with an "Open in Colab" badge.

## [0.1.0]

### Added
- Initial release: typed Python client generated from the Attack-Data API OpenAPI spec (`list_benchmarks`, `get_catalog`, `list_items`, `download_item`, `get_usage`; sync + async). Cursor auto-pagination on `list_items`.

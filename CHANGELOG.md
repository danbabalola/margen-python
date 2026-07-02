# Changelog

All notable changes to the `margen` Python SDK. Versioning follows SemVer; the
SDK version is decoupled from the API version. See the API's own versioning
policy for the wire contract.

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

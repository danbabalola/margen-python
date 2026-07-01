# Margen SDK

## Overview

Margen Attack-Data API: Credit-metered API that delivers labeled deepfake attack-data (real vs AI-generated face images and their platform-perturbed variants). Data is organized into benchmarks (versioned datasets, e.g. synthetic-face-v1), each with its own queryable dimensions. Reverse-engineered from the live b2b-website routes and the proven scripts/data-api/margen_client.py; this spec is the source of truth for the generated SDKs. Auth: Bearer token (or x-api-key). Pull one image per credit; test keys pull a free fixed sample. The canonical path prefix is /api/v1/data; the unversioned /api/data prefix remains a permanent alias.

### Available Operations

* [list_benchmarks](#list_benchmarks) - List benchmarks the key can query
* [get_catalog](#get_catalog) - Dimensions and allowed values for a benchmark
* [list_items](#list_items) - Select items for a benchmark
* [download_item](#download_item) - Get a signed URL for one item
* [get_usage](#get_usage) - Current tier and credit balance

## list_benchmarks

Returns the benchmarks visible to the key. Pick an id and pass it as the `benchmark` parameter on /catalog and /items.

### Example Usage

<!-- UsageSnippet language="python" operationID="listBenchmarks" method="get" path="/api/v1/data/benchmarks" -->
```python
from margen import Margen
import os


with Margen(
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.list_benchmarks()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.BenchmarkList](../../models/benchmarklist.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.Error              | 401, 429                  | application/json          |
| errors.MargenDefaultError | 4XX, 5XX                  | \*/\*                     |

## get_catalog

Self-describing catalog for one benchmark: each dimension with its allowed values, plus a `filters` map of query-param to allowed values. This is the runtime source of truth for what a benchmark supports (the API is registry-driven; do not hardcode dimension values in a client).

### Example Usage

<!-- UsageSnippet language="python" operationID="getCatalog" method="get" path="/api/v1/data/catalog" -->
```python
from margen import Margen
import os


with Margen(
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.get_catalog()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                           | Type                                                                                                                                                                                                | Required                                                                                                                                                                                            | Description                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `benchmark`                                                                                                                                                                                         | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Benchmark id (e.g. synthetic-face-v1). Effectively required: omitting it works only while the key sees exactly one benchmark; once a second exists, omission returns 400 listing the available ids. |
| `retries`                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                 |

### Response

**[models.Catalog](../../models/catalog.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.Error              | 400, 401, 404, 429        | application/json          |
| errors.MargenDefaultError | 4XX, 5XX                  | \*/\*                     |

## list_items

Filterable list of items (ids + attributes, no storage paths). Any filter accepts a comma-separated list, which matches any of the values (OR within a dimension); separate params must all hold (AND across dimensions). Omit a dimension to include all of its values. Fixed dimensions validate and return 400 on an unknown value.

Dimension filters are benchmark-defined: the ones below cover synthetic-face-v1; call /catalog for a benchmark's actual dimensions and values. Additional per-benchmark dimensions are queried by their catalog `key`.

Pagination has three modes: (1) offset (default: `limit`/`offset`, exact `total`, `has_more`; no cursor), (2) cursor (`cursor` set: keyset, `total` null, `next_cursor` set), (3) lineage (`lineage=true`: pages whole lineages; `limit`/`offset` count lineages, `total_lineages`/`lineages` returned, no cursor).

The x-speakeasy-pagination extension on this operation describes cursor mode only: a generated SDK auto-pages by feeding `next_cursor` back into the `cursor` query param. Offset and lineage modes are paged manually.

### Example Usage

<!-- UsageSnippet language="python" operationID="listItems" method="get" path="/api/v1/data/items" -->
```python
from margen import Margen
import os


with Margen(
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.list_items(limit=100, offset=0)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                                                                                                                                                           | Type                                                                                                                                                                                                | Required                                                                                                                                                                                            | Description                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `benchmark`                                                                                                                                                                                         | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Benchmark id (e.g. synthetic-face-v1). Effectively required: omitting it works only while the key sees exactly one benchmark; once a second exists, omission returns 400 listing the available ids. |
| `skin_tone`                                                                                                                                                                                         | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Demographic cell skin-tone band(s), comma-separated. Values per /catalog (e.g. very_light,light,intermediate,tan,brown,dark).                                                                       |
| `gender`                                                                                                                                                                                            | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Demographic cell gender(s), comma-separated (e.g. female,male).                                                                                                                                     |
| `kind`                                                                                                                                                                                              | [Optional[models.ListItemsKind]](../../models/listitemskind.md)                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | real (genuine, unmodified) or fake (AI-generated). Comma-separated allowed.                                                                                                                         |
| `generator`                                                                                                                                                                                         | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Generator model(s) (fake only). Values per /catalog.                                                                                                                                                |
| `perturbation`                                                                                                                                                                                      | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Condition(s) applied. Values per /catalog (e.g. clean,jpeg_q70,fb_pipeline). Alias: `condition`.                                                                                                    |
| `condition`                                                                                                                                                                                         | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Alias for `perturbation`.                                                                                                                                                                           |
| `layer`                                                                                                                                                                                             | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Perturbation layer(s) (clean, layer1, layer2, layer2_recropped).                                                                                                                                    |
| `source_real_id`                                                                                                                                                                                    | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Pull the full lineage descended from one sourced real image.                                                                                                                                        |
| `limit`                                                                                                                                                                                             | *Optional[int]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Page size. Values above 500 are clamped; the response sets limit_clamped.                                                                                                                           |
| `offset`                                                                                                                                                                                            | *Optional[int]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Pagination offset (offset/lineage modes).                                                                                                                                                           |
| `cursor`                                                                                                                                                                                            | *Optional[str]*                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                  | Keyset cursor from a prior response's next_cursor (cursor mode).                                                                                                                                    |
| `lineage`                                                                                                                                                                                           | [Optional[models.Lineage]](../../models/lineage.md)                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                  | Set to true to page over whole lineages.                                                                                                                                                            |
| `retries`                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                 |

### Response

**[models.ListItemsResponse](../../models/listitemsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.Error              | 400, 401, 404, 429        | application/json          |
| errors.MargenDefaultError | 4XX, 5XX                  | \*/\*                     |

## download_item

Returns JSON with a short-lived signed URL (not the image bytes). Fetch `url` with a plain HTTP client and NO auth header, within `expires_in` seconds. On the live tier this debits one credit before returning the URL; test items are free. Send an Idempotency-Key header so a retry of the same item is a no-op (not a second charge). On a zero balance returns 402 with code insufficient_credits.

### Example Usage

<!-- UsageSnippet language="python" operationID="downloadItem" method="get" path="/api/v1/data/download/{itemId}" -->
```python
from margen import Margen
import os


with Margen(
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.download_item(item_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                  | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `item_id`                                                                  | *str*                                                                      | :heavy_check_mark:                                                         | The item id from /items.                                                   |
| `idempotency_key`                                                          | *Optional[str]*                                                            | :heavy_minus_sign:                                                         | Stable per item across retries so a retried download is not charged twice. |
| `retries`                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)           | :heavy_minus_sign:                                                         | Configuration to override the default retry behavior of the client.        |

### Response

**[models.Download](../../models/download.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.Error              | 401, 402, 403, 404, 429   | application/json          |
| errors.MargenDefaultError | 4XX, 5XX                  | \*/\*                     |

## get_usage

The key owner's tier and credit balance. Check before a large pull to avoid a mid-run 402.

### Example Usage

<!-- UsageSnippet language="python" operationID="getUsage" method="get" path="/api/v1/data/usage" -->
```python
from margen import Margen
import os


with Margen(
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.get_usage()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Usage](../../models/usage.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.Error              | 401, 429                  | application/json          |
| errors.MargenDefaultError | 4XX, 5XX                  | \*/\*                     |
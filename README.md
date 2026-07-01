# margen

Developer-friendly & type-safe Python SDK specifically catered to leverage *margen* API.

[![Built by Speakeasy](https://img.shields.io/badge/Built_by-SPEAKEASY-374151?style=for-the-badge&labelColor=f3f4f6)](https://www.speakeasy.com/?utm_source=margen&utm_campaign=python)
[![License: MIT](https://img.shields.io/badge/LICENSE_//_MIT-3b5bdb?style=for-the-badge&labelColor=eff6ff)](https://opensource.org/licenses/MIT)

<!-- Start Summary [summary] -->
## Summary

Margen Attack-Data API: Credit-metered API that delivers labeled deepfake attack-data (real vs AI-generated face images and their platform-perturbed variants). Data is organized into benchmarks (versioned datasets, e.g. synthetic-face-v1), each with its own queryable dimensions. Auth: Bearer token. Pull one image per credit; test keys pull a free fixed sample. The canonical path prefix is /api/v1/data; the unversioned /api/data prefix remains a permanent alias.
<!-- End Summary [summary] -->

## Notebook quickstart & bulk downloads

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/danbabalola/margen-python/blob/main/notebooks/quickstart.ipynb)

Beyond the generated client, `margen.ergonomics` adds notebook-friendly helpers (paginated iteration + one-call bulk download):

```python
from margen import Margen
from margen.ergonomics import iter_items, download_selection

client = Margen(bearer_auth="mgn_test_...")   # your key from margensoftware.com/keys

picks = list(iter_items(client, benchmark="synthetic-face-v1", kind="fake", skin_tone="dark"))
download_selection(client, picks, "out/")     # signed-URL fetch, deterministic idempotency, stop-on-402
```

- `iter_items(client, **filters)` / `iter_lineages(client, **filters)` — yield the whole result set, paging under the hood.
- `download_selection(client, items, out_dir)` — download a selection to a folder; previews cleanly in Colab. Run `notebooks/quickstart.ipynb`.

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [margen](#margen)
  * [SDK Installation](#sdk-installation)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Pagination](#pagination)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!TIP]
> To finish publishing your SDK to PyPI you must [run your first generation action](https://www.speakeasy.com/docs/github-setup#step-by-step-guide).


> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with *uv*, *pip*, or *poetry* package managers.

### uv

*uv* is a fast Python package installer and resolver, designed as a drop-in replacement for pip and pip-tools. It's recommended for its speed and modern Python tooling capabilities.

```bash
uv add git+<UNSET>.git
```

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install git+<UNSET>.git
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add git+<UNSET>.git
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from margen python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "margen",
# ]
# ///

from margen import Margen

sdk = Margen(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from margen import Margen
import os


with Margen(
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.list_benchmarks()

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from margen import Margen
import os

async def main():

    async with Margen(
        bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
    ) as m_client:

        res = await m_client.list_benchmarks_async()

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name          | Type | Scheme      | Environment Variable |
| ------------- | ---- | ----------- | -------------------- |
| `bearer_auth` | http | HTTP Bearer | `MARGEN_BEARER_AUTH` |

To authenticate with the API the `bearer_auth` parameter must be set when initializing the SDK client instance. For example:
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
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [Margen SDK](docs/sdks/margen/README.md)

* [list_benchmarks](docs/sdks/margen/README.md#list_benchmarks) - List benchmarks the key can query
* [get_catalog](docs/sdks/margen/README.md#get_catalog) - Dimensions and allowed values for a benchmark
* [list_items](docs/sdks/margen/README.md#list_items) - Select items for a benchmark
* [download_item](docs/sdks/margen/README.md#download_item) - Get a signed URL for one item
* [get_usage](docs/sdks/margen/README.md#get_usage) - Current tier and credit balance

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Pagination [pagination] -->
## Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
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
<!-- End Pagination [pagination] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from margen import Margen
from margen.utils import BackoffStrategy, RetryConfig
import os


with Margen(
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.list_benchmarks(,
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from margen import Margen
from margen.utils import BackoffStrategy, RetryConfig
import os


with Margen(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.list_benchmarks()

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`MargenError`](./src/margen/errors/margenerror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                                                             |
| ------------------ | ---------------- | --------------------------------------------------------------------------------------- |
| `err.message`      | `str`            | Error message                                                                           |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                                                      |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                                                   |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned.                                  |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                                                       |
| `err.data`         |                  | Optional. Some errors may contain structured data. [See Error Classes](#error-classes). |

### Example
```python
from margen import Margen, errors
import os


with Margen(
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:
    res = None
    try:

        res = m_client.list_benchmarks()

        # Handle response
        print(res)


    except errors.MargenError as e:
        # The base class for HTTP error responses
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)

        # Depending on the method different errors may be thrown
        if isinstance(e, errors.Error):
            print(e.data.error)  # str
            print(e.data.code)  # models.Code
            print(e.data.param)  # Optional[str]
            print(e.data.allowed)  # Optional[List[str]]
            print(e.data.available)  # Optional[List[models.Available]]
```

### Error Classes
**Primary errors:**
* [`MargenError`](./src/margen/errors/margenerror.py): The base class for HTTP error responses.
  * [`Error`](./src/margen/errors/error.py): Missing, invalid, or revoked API key.

<details><summary>Less common errors (5)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`MargenError`](./src/margen/errors/margenerror.py)**:
* [`ResponseValidationError`](./src/margen/errors/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Index

You can override the default server globally by passing a server index to the `server_idx: int` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the indexes associated with the available servers:

| #   | Server                       | Description |
| --- | ---------------------------- | ----------- |
| 0   | `https://margensoftware.com` | Production  |
| 1   | `http://localhost:3000`      | Local dev   |

#### Example

```python
from margen import Margen
import os


with Margen(
    server_idx=0,
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.list_benchmarks()

    # Handle response
    print(res)

```

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from margen import Margen
import os


with Margen(
    server_url="http://localhost:3000",
    bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
) as m_client:

    res = m_client.list_benchmarks()

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from margen import Margen
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Margen(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from margen import Margen
from margen.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Margen(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Margen` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from margen import Margen
import os
def main():

    with Margen(
        bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
    ) as m_client:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Margen(
        bearer_auth=os.getenv("MARGEN_BEARER_AUTH", ""),
    ) as m_client:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from margen import Margen
import logging

logging.basicConfig(level=logging.DEBUG)
s = Margen(debug_logger=logging.getLogger("margen"))
```

You can also enable a default debug logger by setting an environment variable `MARGEN_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=margen&utm_campaign=python)

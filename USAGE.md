<!-- Start SDK Example Usage [usage] -->
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
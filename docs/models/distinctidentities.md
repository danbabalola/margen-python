# DistinctIdentities

Set to true to return ONE representative item per identity_id (dedupe by person; opt-in, no default cap). Composes with filters (e.g. + kind=real returns one real per person). Deterministic representative. Response sets mode=distinct_identities with total_identities; paginate with limit/offset over identities.

## Example Usage

```python
from margen.models import DistinctIdentities
value: DistinctIdentities = "true"
```


## Values

- `"true"`

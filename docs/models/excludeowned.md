# ExcludeOwned

Offset mode only. Omit items you already own (credits are used per unique image, so owned items are free re-downloads). The response adds remaining/owned/total_matching and subset_exhausted with a message when you own the whole matching subset.

## Example Usage

```python
from margen.models import ExcludeOwned
value: ExcludeOwned = "true"
```


## Values

- `"true"`

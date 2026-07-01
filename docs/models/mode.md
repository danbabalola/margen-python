# Mode

## Example Usage

```python
from margen.models import Mode

# Open enum: unrecognized values are captured as UnrecognizedStr
value: Mode = "offset"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"offset"`
- `"cursor"`
- `"lineage"`

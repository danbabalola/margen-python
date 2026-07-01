# Code

Stable machine-readable error code. Branch on this, not on the message text.

## Example Usage

```python
from margen.models import Code

# Open enum: unrecognized values are captured as UnrecognizedStr
value: Code = "unauthorized"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"unauthorized"`
- `"insufficient_credits"`
- `"forbidden_tier"`
- `"not_found"`
- `"unknown_benchmark"`
- `"ambiguous_benchmark"`
- `"invalid_param"`
- `"invalid_cursor"`
- `"rate_limited"`
- `"service_unconfigured"`
- `"server_error"`

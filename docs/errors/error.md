# Error

Missing, invalid, or revoked API key.


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `error`                                                                        | *str*                                                                          | :heavy_check_mark:                                                             | Human-readable message.                                                        |
| `code`                                                                         | [models.Code](../models/code.md)                                               | :heavy_check_mark:                                                             | Stable machine-readable error code. Branch on this, not on the message text.   |
| `param`                                                                        | *Optional[str]*                                                                | :heavy_minus_sign:                                                             | The offending query param (invalid_param on an unknown fixed-dimension value). |
| `allowed`                                                                      | List[*str*]                                                                    | :heavy_minus_sign:                                                             | Allowed values for the offending param (invalid_param).                        |
| `available`                                                                    | List[[models.Available](../models/available.md)]                               | :heavy_minus_sign:                                                             | Available benchmarks (unknown_benchmark / ambiguous_benchmark).                |
| `required`                                                                     | *Optional[int]*                                                                | :heavy_minus_sign:                                                             | Credits required (insufficient_credits).                                       |
# AttackDataItem


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `object`                                                   | *Literal["attack_data_item"]*                              | :heavy_check_mark:                                         | N/A                                                        |
| `id`                                                       | *str*                                                      | :heavy_check_mark:                                         | Pass to /api/v1/data/download/{itemId}.                    |
| `benchmark`                                                | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `kind`                                                     | [models.Kind](../models/kind.md)                           | :heavy_check_mark:                                         | N/A                                                        |
| `skin_tone`                                                | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `gender`                                                   | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `generator`                                                | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | Generator model (fake only).                               |
| `perturbation`                                             | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `layer`                                                    | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `source_real_id`                                           | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | Lineage key; all variants of one source share it.          |
| `source_dataset`                                           | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | Provenance / license source (e.g. pexels).                 |
| `attributes`                                               | Dict[str, *Any*]                                           | :heavy_minus_sign:                                         | Benchmark-specific fields; {} when the benchmark has none. |
# CatalogDimension


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `key`                                                      | *str*                                                      | :heavy_check_mark:                                         | The query-param name.                                      |
| `label`                                                    | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `source`                                                   | [models.Source](../models/source.md)                       | :heavy_check_mark:                                         | N/A                                                        |
| `alias`                                                    | *Optional[str]*                                            | :heavy_minus_sign:                                         | N/A                                                        |
| `values`                                                   | List[[models.DimensionValue](../models/dimensionvalue.md)] | :heavy_minus_sign:                                         | Allowed values (labeled). Absent for lineage keys.         |
| `lineage`                                                  | *Optional[bool]*                                           | :heavy_minus_sign:                                         | N/A                                                        |
| `note`                                                     | *Optional[str]*                                            | :heavy_minus_sign:                                         | N/A                                                        |
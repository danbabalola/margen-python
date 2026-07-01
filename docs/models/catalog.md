# Catalog


## Fields

| Field                                                          | Type                                                           | Required                                                       | Description                                                    |
| -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| `object`                                                       | *Literal["catalog"]*                                           | :heavy_check_mark:                                             | N/A                                                            |
| `benchmark`                                                    | [models.Benchmark](../models/benchmark.md)                     | :heavy_check_mark:                                             | N/A                                                            |
| `tier`                                                         | [models.CatalogTier](../models/catalogtier.md)                 | :heavy_check_mark:                                             | N/A                                                            |
| `total`                                                        | *Optional[int]*                                                | :heavy_minus_sign:                                             | N/A                                                            |
| `dimensions`                                                   | List[[models.CatalogDimension](../models/catalogdimension.md)] | :heavy_check_mark:                                             | N/A                                                            |
| `filters`                                                      | Dict[str, *Any*]                                               | :heavy_check_mark:                                             | Map of query-param to allowed values (self-describing).        |
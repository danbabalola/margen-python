# Download


## Fields

| Field                                                                   | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `object`                                                                | *Literal["download"]*                                                   | :heavy_check_mark:                                                      | N/A                                                                     |
| `url`                                                                   | *str*                                                                   | :heavy_check_mark:                                                      | Short-lived signed URL for one image (JPEG). Fetch with no auth header. |
| `expires_in`                                                            | *int*                                                                   | :heavy_check_mark:                                                      | Seconds until the signed URL expires (300).                             |
| `item`                                                                  | [models.AttackDataItem](../models/attackdataitem.md)                    | :heavy_check_mark:                                                      | N/A                                                                     |
| `balance`                                                               | *OptionalNullable[int]*                                                 | :heavy_minus_sign:                                                      | Credit balance after the debit; null for free test items.               |
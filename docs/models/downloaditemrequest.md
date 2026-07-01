# DownloadItemRequest


## Fields

| Field                                                                      | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `item_id`                                                                  | *str*                                                                      | :heavy_check_mark:                                                         | The item id from /items.                                                   |
| `idempotency_key`                                                          | *Optional[str]*                                                            | :heavy_minus_sign:                                                         | Stable per item across retries so a retried download is not charged twice. |
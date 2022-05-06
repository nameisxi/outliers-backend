# Architecture

![Alt text](https://raw.githubusercontent.com/nameisxi/outliers-backend/main/documentation/architecture-diagram.svg?token=GHSAT0AAAAAABUI6YOQ4P5MO3IDPWDWGWZGYTU4NDQ)

## Endpoints
### Leads /users/candidates/
```http
GET /users/candidates/?format='json'&limit=10&language=python&language=java&topic=android
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `format` | `string` | **Optional**. API output format filter. Possible values: 'json' and 'api'. |
| `limit` | `integer` | **Optional**. Response size filter. Possible values: 1 <= limit <= inf. |
| `language` | `string` | **Optional**. Candidate programming language filter. Possible values: programming language names. |
| `topic` | `string` | **Optional**. Candidate topic filter. Possible values: Github topic names. |

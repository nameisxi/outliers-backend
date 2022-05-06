# Architecture

## Endpoints
```http
GET /users/candidates/?format='json'&limit=10&language=python&language=java&topic=android
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `format` | `string` | **Optional**. API output format filter. Possible values: 'json' and 'api'. |
| `limit` | `integer` | **Optional**. Response size filter. Possible values: 1 <= limit <= inf. |
| `language` | `string` | **Optional**. Candidate programming language filter. Possible values: programming language names. |
| `topic` | `string` | **Optional**. Candidate topic filter. Possible values: Github topic names. |

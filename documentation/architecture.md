# Architecture

![Alt text](https://raw.githubusercontent.com/nameisxi/outliers-backend/bed1515fc56ea4a86caff551b48ece7e7bd9a645/documentation/architecture-diagram.svg?token=AIGB5BNZZQQA6QT4CRVVQPTCOT7NE)

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

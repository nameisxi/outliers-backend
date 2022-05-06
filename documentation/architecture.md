# Architecture doc

![Alt text](https://raw.githubusercontent.com/nameisxi/outliers-backend/bed1515fc56ea4a86caff551b48ece7e7bd9a645/documentation/architecture-diagram.svg?token=AIGB5BNZZQQA6QT4CRVVQPTCOT7NE)

## Endpoints
### Leads endpoint
```http
GET /users/candidates/?format='json'&limit=10&language=python&language=java&topic=android
```
#### Request
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `format` | `string` | **Optional**. API output format filter. Possible values: 'json' and 'api'. |
| `limit` | `integer` | **Optional**. Response size filter. Possible values: 1 <= limit <= inf. |
| `language` | `string` | **Optional**. Candidate programming language filter. Possible values: programming language names. |
| `topic` | `string` | **Optional**. Candidate topic filter. Possible values: Github topic names. |

#### Response
```json
{
    "count": 5,
    "next": "http://localhost:8000/users/candidates/?limit=1&offset=1",
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Junho Yeo",
            "location": "Seoul, Korea",
            "email": "i@junho.io",
            "github_url": "https://github.com/junhoyeo",
            "linkedin_url": null,
            "website_url": "",
            "employer": "@alpha-dao",
            "github_accounts": [
                {
                    "id": 2,
                    "programming_languages": [
                        {
                            "language": {
                                "name": "go"
                            },
                            "language_share": 0.002272398436660888
                        },
                        {
                            "language": {
                                "name": "typescript"
                            },
                            "language_share": 0.8388984903640542
                        }
                    ],
                    "technologies": [
                        {
                            "technology": {
                                "name": "django"
                            },
                            "topic_share": 0.401323423432483007
                        },
                    ],
                    "topics": [
                        {
                            "topic": {
                                "name": "youtube-music-api"
                            },
                            "topic_share": 0.004310344827586207
                        },
                        {
                            "topic": {
                                "name": "youtube-music"
                            },
                            "topic_share": 0.004310344827586207
                        }                    
                    ]
                }
            ],
            "created_at": "2022-05-06T07:08:51.997006Z",
            "updated_at": "2022-05-06T08:25:22.360890Z",
            "work_score": 0.07760621741508444,
            "popularity_score": 0.1297260928771628,
            "hireability_score": -1.0,
            "fit_score": -1.0
        }
    ]
}
```

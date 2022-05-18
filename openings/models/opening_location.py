from django.db import models

from .base_model import BaseModel


class OpeningLocation(BaseModel):
    countries = [
        ('kr', 'South-Korea'),
    ]

    cities = [
        ('seoul', 'Seoul')
    ]

    country = models.CharField(max_length=255, choices=countries)
    city = models.CharField(max_length=255, choices=cities)

from django.db import models

from .base_model import BaseModel


class GithubContributionsCalendar(BaseModel):
    year = models.IntegerField()
    daily_min = models.IntegerField(null=True)
    daily_max = models.IntegerField(null=True)
    daily_median = models.IntegerField(null=True)
    contributions_count = models.BigIntegerField()
    contributions = models.JSONField()

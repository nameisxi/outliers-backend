from django.db import models

from .base_model import BaseModel


class Candidate(BaseModel):
    work_score = models.FloatField()
    popularity_score = models.FloatField()
    hireability_score = models.FloatField()
    fit_score = models.FloatField()
 
    # profile = models.OneToOneField()
    # pre_profile = models.OneToOneField()

    class Meta:
        ordering = ['-work_score']

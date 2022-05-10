from django.db import models

from .candidate_profile import PreProfile
from .base_model import BaseModel


class Candidate(BaseModel):
    work_score = models.FloatField()
    popularity_score = models.FloatField()
    hireability_score = models.FloatField()
    fit_score = models.FloatField()
 
    # profile = models.OneToOneField()
    pre_profile = models.OneToOneField(PreProfile, related_name='candidate', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-work_score']

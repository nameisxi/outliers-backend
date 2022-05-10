from django.db import models

from .candidate_profile import CandidatePreProfile
from .base_model import BaseModel


class Candidate(BaseModel):
    work_score = models.FloatField()
    popularity_score = models.FloatField()
    hireability_score = models.FloatField()
    fit_score = models.FloatField()
 
    # profile = models.OneToOneField()
    pre_profile = models.OneToOneField(CandidatePreProfile, related_name='candidate', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-work_score']

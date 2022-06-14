from django.db import models
from django.contrib.auth.models import User

from .candidate_profile import CandidateProfile, CandidatePreProfile
from .base_model import BaseModel


class Candidate(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile = models.OneToOneField(CandidateProfile, related_name='candidate', on_delete=models.CASCADE, null=True)
    pre_profile = models.OneToOneField(CandidatePreProfile, related_name='candidate', on_delete=models.CASCADE, null=True)
    #TODO: remove models.CASCADE
    # github_account = models.OneToOneField(GithubAccount, related_name='candidate', on_delete=models.CASCADE, null=True)

    work_score = models.FloatField(null=True)
    popularity_score = models.FloatField(null=True)
    hireability_score = models.FloatField(null=True)
    fit_score = models.FloatField(null=True)

    class Meta:
        ordering = ['-work_score']

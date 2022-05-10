from django.db import models

from .base_model import BaseModel


class CandidateProfile(BaseModel):
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    website_url = models.CharField(max_length=255, null=True)
    github_url = models.CharField(max_length=255, null=True)
    linkedin_url = models.CharField(max_length=255, null=True)
    employer = models.CharField(max_length=255, null=True)
    verified_job_looker = models.BooleanField(null=True)

    # class Meta:
    #     abstract = True


class CandidatePreProfile(BaseModel):
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    website_url = models.CharField(max_length=255, null=True)
    github_url = models.CharField(max_length=255, null=True)
    linkedin_url = models.CharField(max_length=255, null=True)
    employer = models.CharField(max_length=255, null=True)
    verified_job_looker = models.BooleanField(null=True)

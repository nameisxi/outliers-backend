from django.db import models

from .base_model import BaseModel


class GithubOrganization(BaseModel):
    organization_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)

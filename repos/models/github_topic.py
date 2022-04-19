from django.db import models

from .base_model import BaseModel


class GithubTopic(BaseModel):
    name = models.CharField(max_length=255)
    
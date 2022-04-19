from django.db import models

from .base_model import BaseModel


class GithubProgrammingLanguage(BaseModel):
    name = models.CharField(max_length=255)
    
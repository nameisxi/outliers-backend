from django.db import models

from .base_model import BaseModel


class ProgrammingLanguage(BaseModel):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255, null=True)
    
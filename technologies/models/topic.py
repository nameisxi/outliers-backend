from django.db import models

from .base_model import BaseModel


class Topic(BaseModel):
    name = models.CharField(max_length=255)
    
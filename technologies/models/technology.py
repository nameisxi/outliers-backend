from django.db import models

from .base_model import BaseModel


class Technology(BaseModel):
    name = models.CharField(max_length=255)
    
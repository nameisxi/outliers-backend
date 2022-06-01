from django.db import models
from django.contrib.auth.models import User

from .base_model import BaseModel
from .company import Company


class Employee(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    last_visit = models.DateTimeField(null=True)

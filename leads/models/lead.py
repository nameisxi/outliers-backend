from django.db import models

from users.models import Candidate, Employee
from openings.models import Opening
from .base_model import BaseModel


class Lead(BaseModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    opening = models.ForeignKey(Opening, related_name='leads', on_delete=models.CASCADE)
    opened_by = models.ManyToManyField(Employee)
    saved = models.BooleanField(default=False)

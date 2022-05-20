from secrets import choice
from django.db import models

from users.models import Candidate, Employee
from .opening import Opening
from .base_model import BaseModel


class OpeningCandidate(BaseModel):
    stages = [
        ('Lead', 'Lead'),
    ]

    opening = models.ForeignKey(Opening, related_name='candidates', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    opened_by = models.ManyToManyField(Employee)

    saved = models.BooleanField(default=False)
    stage = models.CharField(max_length=255, choices=stages)
    
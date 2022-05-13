from django.db import models

from users.models import Candidate, Employee, Company
from technologies.models import ProgrammingLanguage, Technology, Topic
from .base_model import BaseModel


class Opening(BaseModel):
    opening_statuses = [
        ('Sourcing', 'Sourcing'),
        ('Screening', 'Screening'),
        ('Interviewing', 'Interviewing'),
        ('Selecting', 'Selecting'),
        ('Closed', 'Closed'),
    ]

    company = models.ForeignKey(Company, related_name='openings', on_delete=models.CASCADE)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    # leads = models.ManyToManyField(Lead, related_name='openings', on_delete=models.CASCADE)

    status = models.CharField(max_length=255, choices=opening_statuses)
    title = models.CharField(max_length=255)
    team = models.CharField(max_length=255)

    description = models.TextField()
    years_of_experience = models.IntegerField()

    programming_languages = models.ManyToManyField(ProgrammingLanguage, related_name='openings')
    technologies = models.ManyToManyField(Technology, related_name='openings')
    topics = models.ManyToManyField(Topic, related_name='openings')

    base_compensation = models.IntegerField()
    equity_compensation = models.IntegerField()
    other_compensation = models.IntegerField()


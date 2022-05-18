from django.db import models

from users.models import Employee, Company
from technologies.models import ProgrammingLanguage, Technology, Topic
from .opening_location import OpeningLocation
from .base_model import BaseModel


class Opening(BaseModel):
    opening_statuses = [
        ('Sourcing', 'Sourcing'),
        ('Screening', 'Screening'),
        ('Interviewing', 'Interviewing'),
        ('Selecting', 'Selecting'),
        ('Closed', 'Closed'),
    ]

    # currencies = [
    #     ('usd', 'USD'),
    #     ('eur', 'EUR'),
    #     ('krw', 'KRW'),
    # ]

    company = models.ForeignKey(Company, related_name='openings', on_delete=models.CASCADE)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    # location = models.ForeignKey(OpeningLocation, on_delete=models.CASCADE, null=True)

    status = models.CharField(max_length=255, choices=opening_statuses)
    title = models.CharField(max_length=255)
    team = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    years_of_experience_min = models.IntegerField()
    years_of_experience_max = models.IntegerField(null=True)
    programming_languages = models.ManyToManyField(ProgrammingLanguage, related_name='openings')
    technologies = models.ManyToManyField(Technology, related_name='openings')
    topics = models.ManyToManyField(Topic, related_name='openings')

    # base_compensation_min = models.IntegerField(null=True)
    # base_compensation_max = models.IntegerField(null=True)
    # base_compensation_currency = models.CharField(max_length=3, choices=currencies)
    # equity_compensation_min = models.IntegerField(null=True)
    # equity_compensation_max = models.IntegerField(null=True)
    # equity_compensation_currency = models.CharField(max_length=3, choices=currencies)
    # other_compensation_min = models.IntegerField(null=True)
    # other_compensation_max = models.IntegerField(null=True)
    # other_compensation_currency = models.CharField(max_length=3, choices=currencies)

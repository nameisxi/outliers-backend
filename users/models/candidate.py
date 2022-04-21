from django.db import models

from .base_model import BaseModel


class Candidate(BaseModel):
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    github_url = models.CharField(max_length=255, null=True)
    linkedin_url = models.CharField(max_length=255, null=True)
    website_url = models.CharField(max_length=255, null=True)

    years_of_experience = models.IntegerField(null=True)
    current_title = models.CharField(max_length=255, null=True)
    current_employer = models.CharField(max_length=255, null=True)
    university = models.CharField(max_length=255, null=True)

    # programming_languages = models.ManyToManyField()
    # technologies_and_topics = models.ManyToManyField()

    work_score = models.FloatField()
    popularity_score = models.FloatField()
    hireability_score = models.FloatField()
    fit_score = models.FloatField()

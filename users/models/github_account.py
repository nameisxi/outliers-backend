from django.db import models

from .base_model import BaseModel
from .candidate import Candidate


class GithubAccount(BaseModel):
    owner = models.ForeignKey(Candidate, related_name='github_account', on_delete=models.CASCADE)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)
    website = models.CharField(max_length=255, null=True)
    twitter_username = models.CharField(max_length=255, null=True)
    followers = models.IntegerField()
    hireable = models.BooleanField(null=True)
    repos_count = models.IntegerField()
    gists_count = models.IntegerField()
    programming_languages = models.TextField(null=True)
    technologies = models.TextField(null=True)
    profile_html_url = models.CharField(max_length=255)
    profile_api_url = models.CharField(max_length=255)

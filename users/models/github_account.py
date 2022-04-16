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
    repo_count = models.IntegerField()
    profile_url = models.CharField(max_length=255)
    repos_url = models.CharField(max_length=255)

class GithubRepo(BaseModel):
    owner = models.ForeignKey('GithubAccount', on_delete=models.CASCADE)
    repo_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    stargazers_count = models.IntegerField()
    forks_count = models.IntegerField()
    main_language = models.CharField(max_length=255, null=True)
    topics = models.TextField(null=True)

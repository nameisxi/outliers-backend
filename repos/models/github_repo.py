from django.db import models

from .base_model import BaseModel
from users.models import GithubAccount


class GithubRepo(BaseModel):
    repo_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    stargazers_count = models.IntegerField()
    forks_count = models.IntegerField()
    main_language = models.CharField(max_length=255, null=True)
    topics = models.TextField(null=True)
    repo_html_url = models.CharField(max_length=255)
    repo_api_url = models.CharField(max_length=255)


class GithubRepoContributor(BaseModel):
    account = models.ForeignKey(GithubAccount, on_delete=models.CASCADE)
    repo = models.ForeignKey('GithubRepo', on_delete=models.CASCADE)

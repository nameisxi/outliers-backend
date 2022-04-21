from django.db import models

from .base_model import BaseModel
from .candidate import Candidate


class GithubAccount(BaseModel):
    owner = models.ForeignKey(Candidate, related_name='github_accounts', on_delete=models.CASCADE)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    website = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)
    hireable = models.BooleanField(null=True)
    repos_count = models.IntegerField()
    normalized_repos_count = models.FloatField()
    gists_count = models.IntegerField()
    normalized_gists_count = models.FloatField()
    contributions_count = models.IntegerField()
    normalized_contributions_count = models.IntegerField()
    followers_count = models.IntegerField()
    normalized_followers_count = models.FloatField()
    followers_following_counts_difference = models.IntegerField()
    normalized_followers_following_counts_difference = models.FloatField()
    profile_html_url = models.CharField(max_length=255)
    profile_api_url = models.CharField(max_length=255)

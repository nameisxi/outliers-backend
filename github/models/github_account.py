from django.db import models

from users.models import Candidate
from technologies.models import ProgrammingLanguage, Technology, Topic
from .github_repo import GithubRepo
from .base_model import BaseModel


class GithubAccount(BaseModel):
    owner = models.ForeignKey(Candidate, related_name='github_accounts', on_delete=models.CASCADE)
    repos = models.ManyToManyField(GithubRepo, related_name='collaborators')

    github_account_created_at = models.DateField(null=True)
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
    normalized_contributions_count = models.FloatField()
    
    followers_count = models.IntegerField()
    normalized_followers_count = models.FloatField()
    followers_following_counts_difference = models.IntegerField()
    normalized_followers_following_counts_difference = models.FloatField()
    
    profile_html_url = models.CharField(max_length=255)
    profile_api_url = models.CharField(max_length=255)


class GithubAccountLanguage(BaseModel):
    account = models.ForeignKey('GithubAccount', related_name='programming_languages', on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    language_share = models.FloatField()


class GithubAccountTechnology(BaseModel):
    account = models.ForeignKey('GithubAccount', related_name='technologies', on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    technology_share = models.FloatField()


class GithubAccountTopic(BaseModel):
    account = models.ForeignKey('GithubAccount', related_name='topics', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    topic_share = models.FloatField()

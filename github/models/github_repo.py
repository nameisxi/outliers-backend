from django.db import models
from technologies.models import ProgrammingLanguage, Technology, Topic
from .base_model import BaseModel


class GithubRepo(BaseModel):
    repo_created_at = models.DateTimeField(null=True)
    repo_updated_at = models.DateTimeField(null=True)
    pushed_at = models.DateTimeField(null=True)
    languages_scraped_at = models.DateTimeField(null=True)
    
    repo_id = models.BigIntegerField()
    # TODO: add owner_user_id field
    owner_username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    # Impact
    stargazers_count = models.IntegerField()
    # normalized_stargazers_count = models.FloatField(null=True)
    forks_count = models.IntegerField()
    # normalized_forks_count = models.FloatField(null=True)
    watchers_count = models.IntegerField()
    # normalized_watchers_count = models.FloatField(null=True)

    # Complexity
    # TODO: rename to size_in_kb and get the actual size (for scoring) from language byte breakdown.
    size_in_bytes = models.BigIntegerField()
    # normalized_size_in_bytes = models.FloatField(null=True)
    # programming_languages_count = models.IntegerField()
    # normalized_programming_languages_count = models.FloatField(null=True)

    repo_html_url = models.CharField(max_length=255)
    # TODO: delete api url?
    # repo_api_url = models.CharField(max_length=255)


class GithubRepoLanguage(BaseModel):
    repo = models.ForeignKey('GithubRepo', related_name='programming_languages', on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    language_share = models.FloatField(null=True)
    language_contribution = models.BigIntegerField(null=True)


class GithubRepoTechnology(BaseModel):
    repo = models.ForeignKey('GithubRepo', related_name='technologies', on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)


class GithubRepoTopic(BaseModel):
    repo = models.ForeignKey('GithubRepo', related_name='topics', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

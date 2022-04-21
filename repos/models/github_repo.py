from django.db import models

from .base_model import BaseModel
from .github_topic import GithubTopic
from .github_programming_language import GithubProgrammingLanguage
from users.models import GithubAccount


class GithubRepo(BaseModel):
    repo_id = models.BigIntegerField()
    name = models.CharField(max_length=255)

    main_language = models.ManyToManyField(GithubProgrammingLanguage)
    technologies_and_topics = models.ManyToManyField(GithubTopic)

    stargazers_count = models.IntegerField()
    normalized_stargazers_count = models.FloatField()
    forks_count = models.IntegerField()
    normalized_forks_count = models.FloatField()
    watchers_count = models.IntegerField()
    normalized_watchers_count = models.FloatField()

    size_in_kilobytes = models.BigIntegerField()
    normalized_size_in_kilobytes = models.FloatField()

    repo_html_url = models.CharField(max_length=255)
    repo_api_url = models.CharField(max_length=255)


class GithubRepoContributor(BaseModel):
    account = models.ForeignKey(GithubAccount, related_name='contributions', on_delete=models.CASCADE)
    repo = models.ForeignKey('GithubRepo', on_delete=models.CASCADE)

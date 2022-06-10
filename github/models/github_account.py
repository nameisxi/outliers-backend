from datetime import timedelta

from django.db import models
from django.db.models import Sum, Avg, Count
from django.utils import timezone

from users.models import Candidate
from technologies.models import ProgrammingLanguage, Technology, Topic
from .github_repo import GithubRepo
from .github_organization import GithubOrganization
from .github_contributions_calendar import GithubContributionsCalendar
from .base_model import BaseModel


class GithubAccount(BaseModel):
    owner = models.ForeignKey(Candidate, related_name='github_accounts', on_delete=models.CASCADE)
    repos = models.ManyToManyField(GithubRepo, related_name='collaborators')
    repos_scraped_at = models.DateTimeField(null=True)
    organizations = models.ManyToManyField(GithubOrganization, related_name='members')
    organizations_scraped_at = models.DateTimeField(null=True)
    contributions = models.ManyToManyField(GithubContributionsCalendar, related_name='account')
    contributions_scraped_at = models.DateTimeField(null=True)

    account_created_at = models.DateField(null=True)
    account_scraped_at = models.DateTimeField(null=True)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    website = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)
    hireable = models.BooleanField(null=True)
    profile_html_url = models.CharField(max_length=255)

    # TODO: add max 3y age limitation to all of the following property fields!
    
    ##################################################
    # Quantity
    ##################################################
    @property
    def contributions_count(self):
        contribution_count = self.contributions.filter(year__gte=(timezone.now().year - 3)).aggregate(Sum('contributions_count'))['contributions_count__sum']
        if not contribution_count: 
            return 0
        return contribution_count
    normalized_contributions_count = models.FloatField(null=True)

    @property
    def repos_count(self):
        return self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).count()
    normalized_repos_count = models.FloatField(null=True)

    @property
    def codebase_size(self):
        codebase_size = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).aggregate(Sum('size_in_bytes'))['size_in_bytes__sum']
        if not codebase_size: 
            return 0
        return codebase_size
    normalized_codebase_size = models.FloatField(null=True)

    @property
    def language_count(self):
        return self.programming_languages.all().count()
    normalized_language_count = models.FloatField(null=True)

    @property
    def topic_count(self):
        return self.topics.all().count()
    normalized_topic_count = models.FloatField(null=True)

    ##################################################
    # Impact
    ##################################################
    @property
    def stargazer_count(self):
        stargazer_count = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).aggregate(Sum('stargazers_count'))['stargazers_count__sum']
        if not stargazer_count: 
            return 0
        return stargazer_count
    normalized_stargazer_count = models.FloatField(null=True)

    @property
    def average_stargazer_count(self):
        avg_stargazer_count = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).aggregate(Avg('stargazers_count'))['stargazers_count__avg']
        if not avg_stargazer_count: 
            return 0
        return avg_stargazer_count
    normalized_average_stargazer_count = models.FloatField(null=True)

    @property
    def fork_count(self):
        fork_count = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).aggregate(Sum('forks_count'))['forks_count__sum']
        if not fork_count: 
            return 0
        return fork_count
    normalized_fork_count = models.FloatField(null=True)

    @property
    def average_fork_count(self):
        avg_fork_count = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).aggregate(Avg('forks_count'))['forks_count__avg']
        if not avg_fork_count: 
            return 0
        return avg_fork_count
    normalized_average_fork_count = models.FloatField(null=True)

    @property
    def watcher_count(self):
        watcher_count = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).aggregate(Sum('watchers_count'))['watchers_count__sum']
        if not watcher_count: 
            return 0
        return watcher_count
    normalized_watcher_count = models.FloatField(null=True)

    @property
    def average_watcher_count(self):
        avg_watcher_count = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).aggregate(Avg('watchers_count'))['watchers_count__avg']
        if not avg_watcher_count: 
            return 0
        return avg_watcher_count
    normalized_average_watcher_count = models.FloatField(null=True)

    ##################################################
    # Complexity
    ##################################################
    @property
    def average_codebase_size(self):
        avg_codebase_size = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).aggregate(Avg('size_in_bytes'))['size_in_bytes__avg']
        if not avg_codebase_size: 
            return 0
        return avg_codebase_size
    normalized_average_codebase_size = models.FloatField(null=True)

    @property
    def average_language_count(self):
        avg_language_count = self.repos.filter(pushed_at__gte=timezone.now()-timedelta(days=(365 * 3) + 7)).annotate(language_count=Count('programming_languages')).aggregate(Avg('language_count'))['language_count__avg']
        if not avg_language_count: 
            return 0
        return avg_language_count
    normalized_average_language_count = models.FloatField(null=True)

    # TODO: avg collaborator count
    
    ##################################################
    # Popularity
    ##################################################
    followers_count = models.IntegerField()
    normalized_followers_count = models.FloatField(null=True)
    following_count = models.IntegerField()
    normalized_following_count = models.FloatField(null=True)
    
    @property
    def follower_following_count_difference(self):
        if self.followers_count == -1: self.followers_count = 0
        if self.following_count == -1: self.following_count = 0
        return self.followers_count - self.following_count
    normalized_follower_following_count_difference = models.FloatField(null=True)


class GithubAccountLanguage(BaseModel):
    account = models.ForeignKey('GithubAccount', related_name='programming_languages', on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    language_share = models.FloatField(null=True)
    language_share_current_year = models.FloatField(null=True)
    language_share_second_year = models.FloatField(null=True)
    language_share_third_year = models.FloatField(null=True)


class GithubAccountTechnology(BaseModel):
    account = models.ForeignKey('GithubAccount', related_name='technologies', on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    technology_share = models.FloatField(null=True)


class GithubAccountTopic(BaseModel):
    account = models.ForeignKey('GithubAccount', related_name='topics', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    topic_share = models.FloatField(null=True)

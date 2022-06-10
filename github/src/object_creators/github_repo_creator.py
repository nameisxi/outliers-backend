from datetime import timedelta

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

from technologies.models import ProgrammingLanguage, Topic
from ...models import *


class GithubRepoCreator:
    def __init__(self, language_colors):
        self._language_colors = language_colors

    def _get_aware_date(self, date_str):
        date = parse_datetime(date_str)
        if not is_aware(date):
            date = make_aware(date)
        return date

    def _update_field(self, object, fields_and_values):
        for field, value in fields_and_values.items():
            if not getattr(object, field) or (value and getattr(object, field) != value):
                object.__dict__[field] = value

        return object

    def _create_repo_object(self, repo):
        """
        Takes a dictionary object representing a Github repo from the Github REST API as an input and saves it into the database as a GithubRepo object or updates an already existing object. Created or updated object will be returned.
        """
        fields_and_values = {
            'repo_created_at': repo['created_at'],
            'repo_updated_at': repo['updated_at'],
            'pushed_at': repo['pushed_at'],
            'repo_id': repo['id'],
            'owner_username': repo['owner']['login'],
            'name': repo['name'],
            'stargazers_count': repo['stargazers_count'],
            'forks_count': repo['forks_count'], 
            'watchers_count': repo['watchers_count'], 
            'size_in_bytes': repo['size'], 
            'repo_html_url': repo['html_url'],
        }
        repo_object, created = GithubRepo.objects.get_or_create(
            repo_id=repo['id'],
            defaults=fields_and_values
        )

        if not created:
            repo_object = self._update_field(repo_object, fields_and_values)
            repo_object.save()
        
        return repo_object

    def _create_repo_language_object(self, repo, github_repo, github_account):
        """
        Creates a GithubRepoLanguage object and a GithubAccountLanguage object of a given repo language.
        """
        language = repo['language'].lower().strip()
        try:
            color = self._language_colors[language]['color']
        except Exception as e:
            color = '#ffffff'

        programming_language, _ = ProgrammingLanguage.objects.get_or_create(
            name=language, 
            defaults={
                'name': language,
                'color': color,
            }
        )
        
        fields_and_values = {
            'repo': github_repo,
            'language': programming_language,
            'language_share': None,
            'language_contribution': None,
        }
        repo_language, created = GithubRepoLanguage.objects.get_or_create(
            repo=github_repo,
            language=programming_language, 
            defaults=fields_and_values
        )

        if not created:
            repo_language = self._update_field(repo_language, fields_and_values)
            repo_language.save()

        fields_and_values = {
            'account': github_account,
            'language': programming_language,
            'language_share': None,
            'language_share_current_year': None,
            'language_share_second_year': None,
            'language_share_third_year': None,
        }
        account_language, created = GithubAccountLanguage.objects.get_or_create(
            account=github_account,
            language=programming_language, 
            defaults=fields_and_values
        )

        if not created:
            account_language = self._update_field(account_language, fields_and_values)
            account_language.save()

    def _create_repo_topic_objects(self, repo, github_repo, github_account):
        """
        Creates GithubRepoTopic objects and GithubAccountTopic objects of a given repos topics.
        """
        for topic in repo['topics']:
            topic = topic.lower().strip()
            topic, _ = Topic.objects.get_or_create(name=topic, defaults={'name': topic})
            GithubRepoTopic.objects.update_or_create(
                repo=github_repo,
                topic=topic, 
                defaults={
                    'repo': github_repo,
                    'topic': topic,
                }
            )

            fields_and_values = {
                'account': github_account,
                'topic': topic,
                'topic_share': None,
            }
            account_topic, created = GithubAccountTopic.objects.get_or_create(
                account=github_account,
                topic=topic, 
                defaults=fields_and_values
            )

            if not created:
                account_topic = self._update_field(account_topic, fields_and_values)
                account_topic.save()

    def create_repos(self, repos, data_scraped_at):
        """
        Creates GithubRepo objects of given Github-user/Github-repo pair from the Github REST API.
        """
        print('Creating GithubRepos...')

        tenth = max(round(len(repos) * 0.1), 1)

        for i, user_repos in enumerate(repos):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(repos)) * 100)}%')

            # TODO: migrate to user_id
            username = user_repos['username']
            github_account = GithubAccount.objects.get(username=username)

            for repo in user_repos['repos']:
                # - Forks are not considered personal repos.
                # - Repos without languages are useless to us.
                # - Repos of size < 1000 (bytes) are useless to us.
                # - Repos with no commits during the last 3 years are useless to us.
                if repo['fork'] or not repo['language'] or repo['size'] < 1000 or not repo['pushed_at'] or self._get_aware_date(repo['pushed_at']) < (timezone.now() - timedelta(days=(365 * 3) + 7)): 
                    continue

                # Create a repo with given values, or update an existing one
                github_repo = self._create_repo_object(repo)

                # Create a repo contributor with given values, or update an existing one

                github_account.repos.add(github_repo)
                # Add main programming language of the repo
                self._create_repo_language_object(repo, github_repo, github_account)
                # Add topics of the repo
                # TODO: add a check whether topic is really a topic or a technology, like Django
                if repo['topics']:
                    self._create_repo_topic_objects(repo, github_repo, github_account)

            if len(user_repos['repos']) > 0:
                github_account.repos_scraped_at = data_scraped_at
                github_account.save()

        print('    - Done')
        print(f'        GithubRepo.count() = {GithubRepo.objects.count()}')
        print()

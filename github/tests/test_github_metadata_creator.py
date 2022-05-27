from django.test import TestCase

from technologies.models import ProgrammingLanguage, Technology
from ..models import *
from ..src.object_creators import GithubMetadataCreator, GithubRepoCreator
from .test_github_repo_creator import TestGithubRepoCreator

class TestGithubMetadataCreator(TestCase):
    repos = TestGithubRepoCreator()._generate_github_repo_data(3, 2, 2)
    GithubRepoCreator({}).create_repos(repos)

    def _generate_github_repo_language_data(self, n_users, n_repos, n_languages):
        data = {}
        for user_id in range(1, n_users + 1):
            for repo_id in range(1, n_repos + 1):
                data[int(f'{user_id}{repo_id}')] =  { 'languages': {f'test_github_metadata_creator_language_{language_id}':1 for language_id in range(1, n_languages+1)}}

        return data

    def test_create_programming_languages(self):
        n_users = 3
        n_repos = 2
        n_languages = 2
        repos = self._generate_github_repo_language_data(n_users, n_repos, n_languages)
        metadata_creator = GithubMetadataCreator()
        metadata_creator.create_programming_languages(repos, {})

        assert(GithubRepoLanguage.objects.all().filter(language__name__startswith='test_github_metadata_creator_language_').count() == n_users * n_repos * n_languages)
        assert(GithubAccountLanguage.objects.all().filter(language__name__startswith='test_github_metadata_creator_language_').count() == n_users * n_languages)

        metadata_creator.create_programming_languages(repos, {})

        assert(GithubRepoLanguage.objects.all().filter(language__name__startswith='test_github_metadata_creator_language_').count() == n_users * n_repos * n_languages)
        assert(GithubAccountLanguage.objects.all().filter(language__name__startswith='test_github_metadata_creator_language_').count() == n_users * n_languages)

    def test_calculate_programming_languages_counts(self):
        n_users = 3
        n_repos = 2
        n_languages = 2
        repos = self._generate_github_repo_language_data(n_users, n_repos, n_languages)
        metadata_creator = GithubMetadataCreator()
        metadata_creator.create_programming_languages(repos, {})

        metadata_creator.calculate_programming_languages_counts()

        for repo in GithubRepo.objects.all():
            assert(repo.programming_languages_count == GithubRepoLanguage.objects.all().filter(repo=repo).count())
        
    def test_calculate_programming_languages_shares(self):
        GithubRepoLanguage.objects.all().delete()
        GithubAccountLanguage.objects.all().delete()
        GithubAccountTopic.objects.all().delete()
        ProgrammingLanguage.objects.all().delete()
        Topic.objects.all().delete()

        n_users = 3
        n_repos = 2
        n_languages = 2
        repos = self._generate_github_repo_language_data(n_users, n_repos, n_languages)
        metadata_creator = GithubMetadataCreator()
        metadata_creator.create_programming_languages(repos, {})

        metadata_creator.calculate_programming_languages_shares()

        for account_language in GithubAccountLanguage.objects.all():
            all_contributions = n_repos * n_languages * 1
            language_contributions = n_repos * 1
            language_share = language_contributions / all_contributions

            assert(account_language.language_share == language_share)

    def test_calculate_topics_shares(self):
        Topic.objects.all().delete()
        
        n_users = 3
        n_repos = 2
        n_languages = 2
        repos = self._generate_github_repo_language_data(n_users, n_repos, n_languages)
        metadata_creator = GithubMetadataCreator()
        metadata_creator.create_programming_languages(repos, {})

        metadata_creator.calculate_topics_shares()

        for account_topic in GithubAccountTopic.objects.all():
            repos_count = n_repos
            topic_count = n_repos * 1
            topic_share = topic_count / repos_count
            
            assert(account_topic.topic_share == topic_share)
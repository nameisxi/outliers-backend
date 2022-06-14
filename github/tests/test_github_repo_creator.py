import secrets

from django.test import TestCase

from ..models import *
from ..src.object_creators import GithubRepoCreator, GithubAccountCreator
from .test_github_account_creator import TestGithubAccountCreator


class TestGithubRepoCreator(TestCase):
    users = TestGithubAccountCreator()._generate_github_user_data(3)
    GithubAccountCreator().create_accounts(users, '2022-06-08')

    def _generate_topics(self, n_topics):
        random_topics = [f'test_github_repo_creator_topic-{i}' for i in range(1, n_topics+1)]
        return random_topics 

    def _generate_repo(self, user_id, repo_id, n_topics):
        return {
            "id": int(f'{user_id}{repo_id}'),
            "node_id": "id",
            "name": "name",
            "full_name": "username/name",
            "private": False,
            "owner": {
                "login": "username",
                "id": user_id,
                "node_id": "id",
                "avatar_url": "url",
                "gravatar_id": "",
                "url": "url",
                "html_url": "url",
                "followers_url": "url",
                "following_url": "",
                "gists_url": "",
                "starred_url": "",
                "subscriptions_url": "",
                "organizations_url": "",
                "repos_url": "",
                "events_url": "",
                "received_events_url": "",
                "type": "User",
                "site_admin": False,
            },
            "html_url": "",
            "description": "",
            "fork": False,
            "url": "",
            "forks_url": "",
            "keys_url": "",
            "collaborators_url": "",
            "teams_url": "",
            "hooks_url": "",
            "issue_events_url": "",
            "events_url": "",
            "assignees_url": "",
            "branches_url": "",
            "tags_url": "",
            "blobs_url": "",
            "git_tags_url": "",
            "git_refs_url": "",
            "trees_url": "",
            "statuses_url": "",
            "languages_url": "",
            "stargazers_url": "",
            "contributors_url": "",
            "subscribers_url": "",
            "subscription_url": "",
            "commits_url": "",
            "git_commits_url": "",
            "comments_url": "",
            "issue_comment_url": "",
            "contents_url": "",
            "compare_url": "",
            "merges_url": "",
            "archive_url": "",
            "downloads_url": "",
            "issues_url": "",
            "pulls_url": "",
            "milestones_url": "",
            "notifications_url": "",
            "labels_url": "",
            "releases_url": "",
            "deployments_url": "",
            "created_at": "2021-07-07T08:05:56Z",
            "updated_at": "2022-01-31T14:05:12Z",
            "pushed_at": "2022-04-22T00:41:41Z",
            "git_url": "",
            "ssh_url": "",
            "clone_url": "",
            "svn_url": "",
            "homepage": None,
            "size": 1,
            "stargazers_count": 0,
            "watchers_count": 0,
            "language": "test_github_repo_creator_language",
            "has_issues": True,
            "has_projects": True,
            "has_downloads": True,
            "has_wiki": True,
            "has_pages": False,
            "forks_count": 0,
            "mirror_url": None,
            "archived": None,
            "disabled": None,
            "open_issues_count": 1,
            "license": None,
            "allow_forking": True,
            "is_template": False,
            "topics": self._generate_topics(n_topics),
            "visibility": "public",
            "forks": 0,
            "open_issues": 1,
            "watchers": 0,
            "default_branch": "main",
            "permissions": {
                "admin": False,
                "maintain": False,
                "push": False,
                "triage": False,
                "pull": True
            }
        }

    def _generate_github_repo_data(self, n_users, n_repos, n_topics):
        repo_data = []
        for i in range(1, n_users+1):
            repo_data.append(
                {
                    "user_id": i,
                    "username": f'test_{i}',
                    "repos": [self._generate_repo(i, j, n_topics) for j in range(1, n_repos+1)]
                }
            )

        return repo_data

    def test_create_repos(self):
        n_users = 3
        n_repos = 2
        n_topics = 2
        repos = self._generate_github_repo_data(n_users, n_repos, n_topics)
        repo_creator = GithubRepoCreator({})
        repo_creator.create_repos(repos, '2022-06-08')
    
        assert(GithubRepo.objects.all().count() == n_users * n_repos)
        # assert(GithubRepoContributor.objects.all().count() == n_users * n_repos)
        assert(GithubRepoLanguage.objects.all().count() == n_users * n_repos)
        assert(GithubAccountLanguage.objects.all().filter(language__name='test_github_repo_creator_language').count() == n_users)
        assert(GithubRepoTopic.objects.all().count() == n_users * n_repos * n_topics)
        assert(GithubAccountTopic.objects.all().filter(topic__name__startswith='test_github_repo_creator_topic-').count() == n_users * n_topics)

        repo_creator.create_repos(repos, '2022-06-08')

        assert(GithubRepo.objects.all().count() == n_users * n_repos)
        # assert(GithubRepoContributor.objects.all().count() == n_users * n_repos)
        assert(GithubRepoLanguage.objects.all().count() == n_users * n_repos)
        assert(GithubAccountLanguage.objects.all().filter(language__name='test_github_repo_creator_language').count() == n_users)
        assert(GithubRepoTopic.objects.all().count() == n_users * n_repos * n_topics)
        assert(GithubAccountTopic.objects.all().filter(topic__name__startswith='test_github_repo_creator_topic-').count() == n_users * n_topics)

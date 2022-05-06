from django.test import TestCase

from users.models import Candidate
from ..models import GithubAccount
from ..src import GithubAccountCreator


class TestGithubAccountCreator(TestCase):
    def _generate_github_user_data(self, n):
        user_data = []
        for i in range(1, n+1):
            user_data.append(
                {
                    "login": f"test_{i}",
                    "id": i,
                    "node_id": f"id",
                    "avatar_url": "url",
                    "gravatar_id": "",
                    "url": "url",
                    "html_url": "url",
                    "followers_url": "url",
                    "following_url": "url",
                    "gists_url": "url",
                    "starred_url": "url",
                    "subscriptions_url": "url",
                    "organizations_url": "url",
                    "repos_url": "url",
                    "events_url": "url",
                    "received_events_url": "url",
                    "type": "User",
                    "site_admin": False,
                    "name": "name",
                    "company": "company",
                    "blog": "blog",
                    "location": "location",
                    "email": "email",
                    "hireable": None,
                    "bio": "bio",
                    "twitter_username": "username",
                    "public_repos": 2,
                    "public_gists": i,
                    "followers": i,
                    "following": i,
                    "created_at": "2009-11-10T15:11:02Z",
                    "updated_at": "2022-04-18T03:00:56Z",
                    "contributions_count": i
                }
            )

        return user_data

    def test_create_accounts(self):
        users = self._generate_github_user_data(3)
        account_creator = GithubAccountCreator()
        account_creator.create_accounts(users)

        assert(GithubAccount.objects.all().filter(user_id__gte=1).count() == 3)
        assert(Candidate.objects.all().filter(github_accounts__user_id__gte=1).count() == 3)

        account_creator.create_accounts(users)

        assert(GithubAccount.objects.all().filter(user_id__gte=1).count() == 3)
        assert(Candidate.objects.all().filter(github_accounts__user_id__gte=1).count() == 3)


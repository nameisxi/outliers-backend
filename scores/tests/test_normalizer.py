from django.test import TestCase

from users.models import Candidate
from github.models import GithubAccount
from ..src import Normalizer


class TestNormalizer(TestCase):
    accounts = GithubAccount.objects.all()
    excluded_user_ids = []

    for account in accounts:
        if account.contributions_count == 0 or account.repos_count == 0 or account.codebase_size < account.repos_count * 1000 or account.language_count == 0:
            excluded_user_ids.append(account.user_id)

    accounts = accounts.exclude(user_id__in=excluded_user_ids)

    fields = [
        'contributions_count',
        'repos_count',
        'codebase_size',
        'language_count',
        'topic_count',
        'stargazer_count',
        'average_stargazer_count',
        'fork_count',
        'average_fork_count',
        'watcher_count',
        'average_watcher_count',
        'average_codebase_size',
        'average_language_count',
        'follower_following_count_difference',
    ]

    def test_constructor(self):
        normalizer = Normalizer()

        assert(normalizer._random_state == 42)

    def test_normalize_fields(self):
        normalizer = Normalizer()
        normalizer.normalize_fields(GithubAccount, self.accounts, self.fields)

        for object in self.accounts.all():
            for field in self.fields:
                assert(round(getattr(object, f'normalized_{field}'), 3) >= 0.0)
                assert(round(getattr(object, f'normalized_{field}'), 3) <= 1.0)

    def test_scale_distribution(self):
        pass


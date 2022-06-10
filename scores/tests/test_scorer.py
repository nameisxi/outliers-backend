from django.test import TestCase

from users.models import Candidate
from github.models import GithubAccount
from ..src import Scorer, Normalizer
from ..src.scorers import *


class TestScorer(TestCase):
    def _get_accounts(self):
        accounts = GithubAccount.objects.all()
        excluded_ids = []

        for account in accounts:
            if account.contributions_count == 0 or account.repos_count == 0 or account.codebase_size < account.repos_count * 1000 or account.language_count == 0:
                excluded_ids.append(account.id)

        accounts = accounts.exclude(id__in=excluded_ids)

        return accounts, excluded_ids

    def _setup(self):
        accounts, excluded_github_account_ids = self._get_accounts()

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

        normalizer = Normalizer()
        normalizer.normalize_fields(GithubAccount, accounts, fields)

        candidates = Candidate.objects.exclude(github_accounts__id__in=excluded_github_account_ids)

        return candidates

    def test_constructor(self):
        self._setup()

        scorer = Scorer()
        
        assert(isinstance(scorer._work_scorer, WorkScorer))
        assert(isinstance(scorer._popularity_scorer, PopularityScorer))
        assert(isinstance(scorer._hireability_scorer, HireabilityScorer))
        assert(isinstance(scorer._fit_scorer, FitScorer))

    def test_compute_scores(self):
        candidates = self._setup()

        scorer = Scorer()
        scorer.compute_scores(candidates)

        for candidate in candidates:
            assert(candidate.work_score is not None)
            assert(candidate.popularity_score is not None)

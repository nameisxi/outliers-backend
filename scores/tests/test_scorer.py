from django.test import TestCase

from users.models import Candidate
from ..src import Scorer
from ..src.scorers import *


class TestScorer(TestCase):
    def test_constructor(self):
        scorer = Scorer()
        
        assert(isinstance(scorer._work_scorer, WorkScorer))
        assert(isinstance(scorer._popularity_scorer, PopularityScorer))
        assert(isinstance(scorer._hireability_scorer, HireabilityScorer))
        assert(isinstance(scorer._fit_scorer, FitScorer))

    def test_compute_scores(self):
        scorer = Scorer()
        scorer.compute_scores()

        for candidate in Candidate.objects.all():
            assert(candidate.work_score != -2)
            assert(candidate.popularity_score != -2)

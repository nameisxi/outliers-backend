from users.models import Candidate

from .scorers import *


class Scorer:
    def __init__(self):
        self._work_scorer = WorkScorer()
        self._popularity_scorer = PopularityScorer()
        self._hireability_scorer = HireabilityScorer()
        self._fit_scorer = FitScorer()

    def compute_scores(self):
        """
        Computes ranking scores for every Candidate object.
        """
        for candidate in Candidate.objects.all():
            candidate.work_score = self._work_scorer.calculate_work_score(candidate)
            candidate.popularity_score = self._popularity_scorer.calculate_popularity_score(candidate)
            # candidate.hireability_score = self._hireability_scorer.calculate_hireability_score(candidate)
            # candidate.fit_score = self._fit_scorer.calculate_fit_score(candidate)
            candidate.save()

from django.utils import timezone

from users.models import Candidate
from .scorers import *


class Scorer:
    def __init__(self):
        self._work_scorer = WorkScorer()
        self._popularity_scorer = PopularityScorer()
        self._hireability_scorer = HireabilityScorer()
        self._fit_scorer = FitScorer()

    def compute_scores(self, candidates):
        """
        Computes ranking scores for every Candidate object.
        """
        print('Computing ranking scores...')

        tenth = max(round(len(candidates) * 0.1), 1)

        for i, candidate in enumerate(candidates):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(candidates)) * 100)}% [{timezone.now()}]')

            candidate.work_score = self._work_scorer.calculate_work_score(candidate)
            candidate.popularity_score = self._popularity_scorer.calculate_popularity_score(candidate)
            # candidate.hireability_score = self._hireability_scorer.calculate_hireability_score(candidate)
            # candidate.fit_score = self._fit_scorer.calculate_fit_score(candidate)
            # candidate.save()

        Candidate.objects.bulk_update(candidates, ['work_score', 'popularity_score'])

        print('    - Done')
        print(f'        Computed scores for {len(candidates)} candidates')
        print()

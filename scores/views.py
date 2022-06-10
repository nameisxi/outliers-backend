from django.http import HttpResponse, JsonResponse
from django.db.models import Avg

from users.models import Candidate
from github.models import GithubAccount, GithubRepo

from .src import Normalizer, Scorer


def get_accounts():
    accounts = GithubAccount.objects.all()
    excluded_ids = []

    for account in accounts:
        if account.contributions_count == 0 or account.repos_count == 0 or account.codebase_size < account.repos_count * 1000 or account.language_count == 0:
            excluded_ids.append(account.id)

    accounts = accounts.exclude(id__in=excluded_ids)

    return accounts, excluded_ids

def compute(request):
    """
    Executes the ranking score computation pipeline.
    """    
    accounts, excluded_github_ids = get_accounts()

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

    # Normalize given objects' fields
    normalizer = Normalizer()
    normalizer.normalize_fields(GithubAccount, accounts, fields)

    candidates = Candidate.objects.exclude(github_accounts__id__in=excluded_github_ids)

    # Compute ranking scores for Candidate objects
    scorer = Scorer()
    scorer.compute_scores(candidates)

    avg_work_score = candidates.aggregate(Avg('work_score'))['work_score__avg']
    avg_popularity_score = candidates.aggregate(Avg('popularity_score'))['popularity_score__avg']
    avg_hireability_score = candidates.aggregate(Avg('hireability_score'))['hireability_score__avg']
    avg_fit_score = candidates.aggregate(Avg('fit_score'))['fit_score__avg']
    return HttpResponse(f'Candidate count: {len(candidates)}, Work score avg: {avg_work_score}, Popularity score avg: {avg_popularity_score}, Hireability score avg: {avg_hireability_score}, Fit score avg: {avg_fit_score}')

def get_distributions(request):
    """
    Returns the distributions and the normalized versions of those distributions of the fields used to compute the ranking scores.
    """
    # work_scores = {}
    
    # for candidate in Candidate.objects.exclude(work_score__isnull=True).all():
    #     for account in candidate.github_accounts.all():
    #         work_scores[account.user_id] = candidate.work_score

    work_scores = []
    popularity_scores = []

    for candidate in Candidate.objects.exclude(work_score__isnull=True, work_score__lt=0).all():
        for account in candidate.github_accounts.all():
            work_scores.append(candidate.work_score)
            popularity_scores.append(candidate.popularity_score)

    distributions = {
        'work_score': work_scores,
        'popularity_score': popularity_scores,
    }

    return JsonResponse(distributions)

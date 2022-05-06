from django.http import HttpResponse, JsonResponse
from django.db.models import Avg

from users.models import Candidate
from github.models import GithubAccount, GithubRepo

from .src import Normalizer, Scorer


def compute(request):
    """
    Executes the ranking score computation pipeline.
    """
    objects_and_fields = {
        GithubAccount: [
            'repos_count',
            'gists_count',
            'contributions_count',
            'followers_count',
            'followers_following_counts_difference',
        ],
        GithubRepo: [
            'size_in_kilobytes',
            'programming_languages_count',
            'stargazers_count',
            'forks_count',
            'watchers_count',
        ],
    }

    # Normalize given objects' fields
    normalizer = Normalizer()
    normalizer.normalize_fields(objects_and_fields)

    # Compute ranking scores for Candidate objects
    scorer = Scorer()
    scorer.compute_scores()

    avg_work_score = Candidate.objects.all().aggregate(Avg('work_score'))['work_score__avg']
    avg_popularity_score = Candidate.objects.all().aggregate(Avg('popularity_score'))['popularity_score__avg']
    avg_hireability_score = Candidate.objects.all().aggregate(Avg('hireability_score'))['hireability_score__avg']
    avg_fit_score = Candidate.objects.all().aggregate(Avg('fit_score'))['fit_score__avg']
    return HttpResponse(f'Work score avg: {avg_work_score}, Popularity score avg: {avg_popularity_score}, Hireability score avg: {avg_hireability_score}, Fit score avg: {avg_fit_score}')

def get_distributions(request):
    """
    Returns the distributions and the normalized versions of those distributions of the fields used to compute the ranking scores.
    """
    distributions = {
            'Candidate': {
                'work_score': list(Candidate.objects.all().values_list('work_score', flat=True)),
                'popularity_score': list(Candidate.objects.all().values_list('popularity_score', flat=True)),
                # 'hireability_score': list(Candidate.objects.all().values_list('hireability_score', flat=True)),
                # 'fit_score': list(Candidate.objects.all().values_list('fit_score', flat=True)),
            },
            'GithubAccount': {
                'repos_count': list(GithubAccount.objects.all().values_list('repos_count', flat=True)),
                'normalized_repos_count': list(GithubAccount.objects.all().values_list('normalized_repos_count', flat=True)),
                'gists_count': list(GithubAccount.objects.all().values_list('gists_count', flat=True)),
                'normalized_gists_count': list(GithubAccount.objects.all().values_list('normalized_gists_count', flat=True)),
                'contributions_count': list(GithubAccount.objects.all().values_list('contributions_count', flat=True)),
                'normalized_contributions_count': list(GithubAccount.objects.all().values_list('normalized_contributions_count', flat=True)),
                'followers_count': list(GithubAccount.objects.all().values_list('followers_count', flat=True)),
                'normalized_followers_count': list(GithubAccount.objects.all().values_list('normalized_followers_count', flat=True)),
                'followers_following_counts_difference': list(GithubAccount.objects.all().values_list('followers_following_counts_difference', flat=True)),
                'normalized_followers_following_counts_difference': list(GithubAccount.objects.all().values_list('normalized_followers_following_counts_difference', flat=True)),
            },
            'GithubRepo': {
                'size_in_kilobytes': list(GithubRepo.objects.all().values_list('size_in_kilobytes', flat=True)),
                'normalized_size_in_kilobytes': list(GithubRepo.objects.all().values_list('normalized_size_in_kilobytes', flat=True)),
                'programming_languages_count': list(GithubRepo.objects.all().values_list('programming_languages_count', flat=True)),
                'normalized_programming_languages_count': list(GithubRepo.objects.all().values_list('normalized_programming_languages_count', flat=True)),
                'stargazers_count': list(GithubRepo.objects.all().values_list('stargazers_count', flat=True)),
                'normalized_stargazers_count': list(GithubRepo.objects.all().values_list('normalized_stargazers_count', flat=True)),
                'forks_count': list(GithubRepo.objects.all().values_list('forks_count', flat=True)),
                'normalized_forks_count': list(GithubRepo.objects.all().values_list('normalized_forks_count', flat=True)),
                'watchers_count': list(GithubRepo.objects.all().values_list('watchers_count', flat=True)),
                'normalized_watchers_count': list(GithubRepo.objects.all().values_list('normalized_watchers_count', flat=True)),
            },
    }

    return JsonResponse(distributions)

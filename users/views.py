import json

from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView

from .models import *
from .serializers import *
from .filters import *


class CandidateList(ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filterset_class = CandidateFilter


def create_candidates(request):
    with open('./users/users_v2.json', 'r') as f:
        users = json.load(f)
        
        for user in users:
            candidate_defaults = {
                'name': user['name'],
                'location': user['location'],
                'email': user['email'],
                'github_url': user['html_url'],
                'linkedin_url': None,
                'website_url': user['blog'],
                'years_of_experience': None,
                'current_title': None,
                'current_employer': user['company'],
                'university': None,
                'work_score': -1,
                'popularity_score': -1,
                'hireability_score': -1,
                'fit_score': -1,
            }
            candidate, _ = Candidate.objects.update_or_create(
                github_accounts__user_id=user['id'],
                defaults=candidate_defaults
            )

            github_account_defaults = {
                'owner': candidate,
                'user_id': user['id'],
                'username': user['login'],
                'name': user['name'],
                'location': user['location'],
                'email': user['email'],
                'website': user['blog'],
                'company': user['company'],
                'hireable': user['hireable'],
                'repos_count': user['public_repos'],
                'normalized_repos_count': -1,
                'gists_count': user['public_gists'],
                'normalized_gists_count': -1,
                'contributions_count': user['contributions_count'],
                'normalized_contributions_count': -1,
                'followers_count': user['followers'],
                'normalized_followers_count': -1,
                'followers_following_counts_difference': user['followers'] - user['following'],
                'normalized_followers_following_counts_difference': -1,
                'profile_html_url': user['html_url'],
                'profile_api_url': user['url'],
            }
            GithubAccount.objects.update_or_create(
                user_id=user['id'],
                defaults=github_account_defaults
            )

    
    return HttpResponse(f'Candidate objects:{Candidate.objects.count()}\nGithubAccount objects:{GithubAccount.objects.count()}')

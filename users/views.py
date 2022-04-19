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
                'work_score': None,
                'popularity_score': None,
                'hireability_score': None,
            }
            candidate, _ = Candidate.objects.get_or_create(
                github_account__user_id=user['id'],
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
                'programming_languages': None,
                'technologies_and_topics': None,
                'repos_count': user['public_repos'],
                'gists_count': user['public_gists'],
                'contributions_count': user['contributions_count'],
                'followers_count': user['followers'],
                'following_count': user['following'],
                'profile_html_url': user['html_url'],
                'profile_api_url': user['url'],
            }
            GithubAccount.objects.update_or_create(
                user_id=user['id'],
                defaults=github_account_defaults
            )

    
    return HttpResponse(f'Candidate objects:{Candidate.objects.count()}\nGithubAccount objects:{GithubAccount.objects.count()}')

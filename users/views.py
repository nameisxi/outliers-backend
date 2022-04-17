import json

from django.http import HttpResponse

from .models import *


def get_users(request):
    pass

def create_users(request):
    with open('./users/users.json', 'r') as f:
        users = json.load(f)
        
        for user in users:
            candidate, _ = Candidate.objects.get_or_create(github_account__user_id=user['id'])

            fields = {
                'owner': candidate,
                'user_id': user['id'],
                'username': user['login'],
                'name': user['name'],
                'email': user['email'],
                'location': user['location'],
                'company': user['company'],
                'website': user['blog'],
                'twitter_username': user['twitter_username'],
                'followers': user['followers'],
                'hireable': user['hireable'],
                'repos_count': user['public_repos'],
                'gists_count': user['public_gists'],
                'profile_html_url': user['html_url'],
                'profile_api_url': user['url'],
                
            }

            GithubAccount.objects.update_or_create(
                user_id=user['id'],
                defaults=fields
            )

    
    return HttpResponse(f'Candidate objects:{Candidate.objects.count()}\nGithubAccount objects:{GithubAccount.objects.count()}')

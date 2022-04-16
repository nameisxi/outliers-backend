import json

from django.http import HttpResponse

from .models import *


def create_users(request):
    with open('./users/users.json', 'r') as f:
        users = json.load(f)
        
        for user in users:
            candidate, _ = Candidate.objects.get_or_create(github_account__user_id=user['github_id'])

            fields = {
                'owner': candidate,
                'user_id': user['github_id'],
                'username': user['github_username'],
                'name': user['name'],
                'email': user['email'],
                'location': user['location'],
                'company': user['company'],
                'website': user['website'],
                'twitter_username': user['twitter_username'],
                'followers': user['github_followers'],
                'hireable': user['github_hireable'],
                'repo_count': user['github_repos_count'],
                'profile_url': user['github_url'],
                'repos_url': user['github_repos_url'],
            }

            GithubAccount.objects.update_or_create(
                user_id=user['github_id'],
                defaults=fields
            )

    
    return HttpResponse(f'{Candidate.objects.count()} & {GithubAccount.objects.count()}')

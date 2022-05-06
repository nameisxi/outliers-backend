import json
from github.models import github_account

from users.models import Candidate
from ..models import GithubAccount


class GithubAccountCreator:
    def __init__(self):
        pass

    def create_accounts(self, users): 
        """
        Takes a list of Github REST API JSON objects representing Github user accounts. These JSON objects are used to create GithubAccount objects that will be connected to Candidate objects.
        """  
        print('Creating GithubAccounts...')
        
        tenth = max(round(len(users) * 0.1), 1)

        for i, user in enumerate(users):
            if (i + 1) % tenth == 0:
                print(f'    {((i + 1) / len(users)) * 100}%')

            # Create Candidate object if no Github account with the user_id exists
            candidate, _ = Candidate.objects.update_or_create(
                github_accounts__user_id=user['id'],
                defaults={
                    'work_score': -2,
                    'popularity_score': -2,
                    'hireability_score': -2,
                    'fit_score': -2,
                }
            )

            # Create GithubAccount object if no Github account with the user_id exists 
            GithubAccount.objects.update_or_create(
                user_id=user['id'],
                defaults={
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
            )

        print('    - Done')
        print()

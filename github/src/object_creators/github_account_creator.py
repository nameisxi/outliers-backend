from users.models import Candidate
from ...models import GithubAccount


class GithubAccountCreator:
    def __init__(self):
        pass

    def _update_field(self, object, fields_and_values):
        for field, value in fields_and_values.items():
            if not getattr(object, field) or (value and getattr(object, field) != value):
                object.__dict__[field] = value

        return object

    def create_accounts(self, users, data_scraped_at): 
        """
        Takes a list of Github REST API JSON objects representing Github user accounts. These JSON objects are used to create GithubAccount objects that will be connected to Candidate objects.
        """  
        print('Creating GithubAccounts...')
        
        tenth = max(round(len(users) * 0.1), 1)

        for i, user in enumerate(users):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(users)) * 100)}%')

            # Create Candidate object if no Github account with the user_id exists
            candidate, _ = Candidate.objects.get_or_create(
                github_accounts__user_id=user['id'],
                defaults={
                    'user': None,
                    'profile': None,
                    'pre_profile': None,
                    'work_score': None,
                    'popularity_score': None,
                    'hireability_score': None,
                    'fit_score': None,
                }
            )

            # Create GithubAccount object if no Github account with the user_id exists 
            fields_and_values = {
                'owner': candidate,
                'account_scraped_at': data_scraped_at,
                'account_created_at': user['created_at'].split('T')[0],
                'user_id': user['id'],
                'username': user['login'],
                'name': user['name'],
                'location': user['location'],
                'email': user['email'],
                'website': user['blog'],
                'company': user['company'],
                'hireable': user['hireable'],
                'profile_html_url': user['html_url'],
                'followers_count': user['followers'],
                'following_count': user['following'],
            }
            account, created = GithubAccount.objects.get_or_create(
                user_id=user['id'],
                defaults=fields_and_values
            )

        if not created:
            account = self._update_field(account, fields_and_values)
            account.save()

        print('    - Done:')
        print(f'        GithubAccount.count() = {GithubAccount.objects.count()}')
        print()

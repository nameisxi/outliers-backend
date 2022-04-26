import json

from django.http import HttpResponse, JsonResponse
from django.db.models import Count

from .models import *
from users.models import Candidate


def create_github_accounts(request):
    with open('./github/data/users/users_v3.json', 'r') as f:
        users = json.load(f)
        
        for user in users:
            # Create Candidate object if no Github account with the user_id exists
            candidate, _ = Candidate.objects.update_or_create(
                github_accounts__user_id=user['id'],
                defaults={
                    'name': None,
                    'location': None,
                    'email': None,
                    'github_url': None,
                    'linkedin_url': None,
                    'website_url': None,
                    'years_of_experience': None,
                    'current_title': None,
                    'current_employer': None,
                    'university': None,
                    'work_score': -1,
                    'popularity_score': -1,
                    'hireability_score': -1,
                    'fit_score': -1,
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

    
    return HttpResponse(f'Candidate objects:{Candidate.objects.count()}\nGithubAccount objects:{GithubAccount.objects.count()}')

def create_github_repos(request):
    with open('./github/data/repos/repos_v3.json', 'r') as f:
        users_repos = json.load(f)

        for user_repos in users_repos:
            username = user_repos['username']
            github_account = GithubAccount.objects.get(username=username)

            for repo in user_repos['repos']:
                # Forks are not considered personal repos
                if repo['fork']: continue

                # Create a repo with given values, or update an existing one
                github_repo, _ = GithubRepo.objects.update_or_create(
                    repo_id=repo['id'],
                    defaults={
                        'repo_id': repo['id'],
                        'name': repo['name'],
                        'stargazers_count': repo['stargazers_count'],
                        'normalized_stargazers_count': -1,
                        'forks_count': repo['forks_count'], 
                        'normalized_forks_count': -1,
                        'watchers_count': repo['watchers_count'], 
                        'normalized_watchers_count': -1,
                        'size_in_kilobytes': repo['size'], 
                        'normalized_size_in_kilobytes': -1,
                        'programming_languages_count': 0, 
                        'normalized_programming_languages_count': -1,
                        'repo_html_url': repo['html_url'],
                        'repo_api_url': repo['url'],
                    }
                )

                # Create a repo contributor with given values, or update an existing one
                GithubRepoContributor.objects.update_or_create(
                    repo=github_repo,
                    account=github_account,
                    defaults={
                        'account': github_account,
                        'repo': github_repo
                    }
                )

                # Add main programming language of the repo
                if repo['language']:
                    language = repo['language'].lower().strip()
                    programming_language, _ = ProgrammingLanguage.objects.get_or_create(name=language, defaults={'name': language})
                    GithubRepoLanguage.objects.update_or_create(
                        repo=github_repo,
                        language=programming_language, 
                        defaults={
                            'repo': github_repo,
                            'language': programming_language,
                            'language_share': -1.0,
                        }
                    )

                # Add topics of the repo
                # TODO: add a check whether topic is really a topic or a technology, like Django
                if repo['topics']:
                    for topic in repo['topics']:
                        topic = topic.lower().strip()
                        topic, _ = Topic.objects.get_or_create(name=topic, defaults={'name': topic})
                        GithubRepoTopic.objects.update_or_create(
                            repo=github_repo,
                            topic=topic, 
                            defaults={
                                'repo': github_repo,
                                'topic': topic,
                            }
                        )

    return HttpResponse(f'GithubRepo objects: {GithubRepo.objects.count()}\nGithubRepoContributor objects: {GithubRepoContributor.objects.count()}')

def add_programming_languages(request):
    with open('./github/data/languages/languages_v2.json', 'r') as f:
        repos = json.load(f)

        for repo_id, languages in repos.items():
            try:
                repo = GithubRepo.objects.get(repo_id=repo_id)
            except GithubRepo.DoesNotExist:
                continue

            for repo_languages_object in languages:
                total_contributions_count = sum(list(repo_languages_object.values()))
                if total_contributions_count == 0:
                    continue

                for language, language_contributions_count in repo_languages_object.items():
                    if language_contributions_count == 0:
                        continue

                    language = language.lower().strip()
                    programming_language, _ = ProgrammingLanguage.objects.get_or_create(name=language, defaults={'name': language})

                    # Add programming language relationship with each repo
                    GithubRepoLanguage.objects.update_or_create(
                        repo=repo,
                        language=programming_language, 
                        defaults={
                            'repo': repo,
                            'language': programming_language,
                            'language_share': language_contributions_count / total_contributions_count,
                        }
                    )

                    # Add programming language relationship with each account
                    for contributor in repo.contributors.all():
                        GithubAccountLanguage.objects.update_or_create(
                            account=contributor.account,
                            language=programming_language, 
                            defaults={
                                'account': contributor.account,
                                'language': programming_language,
                            }
                        )

    return HttpResponse(f'ProgrammingLanguage objects: {ProgrammingLanguage.objects.count()}\nGithubRepoLanguage objects: {GithubRepoLanguage.objects.count()}\nGithubAccountLanguage objects: {GithubAccountLanguage.objects.count()}')

def add_programming_languages_counts(request):
    repos = GithubRepo.objects.all()

    for repo in repos:
        repo.programming_languages_count = repo.programming_languages.all().count()
    
    GithubRepo.objects.bulk_update(repos, ['programming_languages_count'])

    return HttpResponse('Completed')


def get_repos_with_common_contributors(request):
    common_repos = []
    counts = GithubRepo.objects.annotate(number_of_common_collaborators=Count('githubrepocontributor'))

    for count in counts:
        if count.number_of_common_collaborators > 1:
            common_repos.append(count.name)

    return HttpResponse(f'{common_repos}, {len(common_repos)}')

def get_contact_details(request):
    emails = list(GithubAccount.objects.all().values_list('email', flat=True))
    websites = list(GithubAccount.objects.all().values_list('website', flat=True))

    return JsonResponse({
        'emails': emails,
        'websites': websites,
    })
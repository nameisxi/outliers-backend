import json

from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum

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
                        GithubAccountTopic.objects.update_or_create(
                            account=github_account,
                            topic=topic, 
                            defaults={
                                'account': github_account,
                                'topic': topic,
                                'topic_share': -1,
                            }
                        )

    return HttpResponse(f'GithubRepo objects: {GithubRepo.objects.count()}\nGithubRepoContributor objects: {GithubRepoContributor.objects.count()}')

def add_programming_languages(request):
    updated_repos = 
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
                    # TODO: if language_contribution_count, e.g. contribution filesize, < x, skip?
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
                                'language_share': -1,
                            }
                        )

    return HttpResponse(f'ProgrammingLanguage objects: {ProgrammingLanguage.objects.count()}\nGithubRepoLanguage objects: {GithubRepoLanguage.objects.count()}\nGithubAccountLanguage objects: {GithubAccountLanguage.objects.count()}')

def add_programming_languages_counts(request):
    repos = GithubRepo.objects.all()
    for repo in repos:
        repo.programming_languages_count = repo.programming_languages.all().count()
    
    GithubRepo.objects.bulk_update(repos, ['programming_languages_count'])

    account_languages = GithubAccountLanguage.objects.all()
    for account_language in account_languages:
        all_contributions = account_language.account.contributions.aggregate(models.Sum('repo__programming_languages__language_share'))['repo__programming_languages__language_share__sum']
        language_contributions = account_language.account.contributions.filter(repo__programming_languages__language=account_language.language).aggregate(models.Sum('repo__programming_languages__language_share'))['repo__programming_languages__language_share__sum']
        
        account_language.language_share = language_contributions / all_contributions
    
    GithubAccountLanguage.objects.bulk_update(account_languages, ['language_share'])

    account_topics = GithubAccountTopic.objects.all()
    for account_topic in account_topics:
        repos_count = account_topic.account.repos_count
        if repos_count == 0: continue
        topic_count = account_topic.account.contributions.filter(repo__topics__topic=account_topic.topic).count()
        
        account_topic.topic_share = topic_count / repos_count
    
    GithubAccountTopic.objects.bulk_update(account_topics, ['topic_share'])

    return HttpResponse('Completed')


def populate(request):
    # create_github_accounts()
    # create_github_repos()
    # add_programming_languages()
    # add_repo_programming_languages_counts()
    # add_account_programming_languages_shares()
    # add_account_topics_shares()
    pass

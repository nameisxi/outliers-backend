import json

from django.http import HttpResponse
from django.db.models import Count

from .models import GithubRepo, GithubRepoContributor
from users.models import GithubAccount


def create_repos(request):
    with open('./repos/repos.json', 'r') as f:
        users_repos = json.load(f)

        for user_repos in users_repos:
            username = user_repos['username']
            github_account = GithubAccount.objects.get(username=username)
            programming_languages = set()
            technologies = set()

            repos = user_repos['repos']

            for repo in repos:
                if repo['fork']: continue

                if repo['language']:
                    programming_languages.add(repo['language'].lower().strip())
                if repo['topics']:
                    for technology in repo['topics']:
                        technologies.add(technology.lower().strip())

                repo_fields = {
                    'repo_id': repo['id'],
                    'name': repo['name'],
                    'stargazers_count': repo['stargazers_count'],
                    'forks_count': repo['forks_count'], 
                    'main_language': repo['language'],
                    'topics': repo['topics'],
                    'repo_html_url': repo['html_url'],
                    'repo_api_url': repo['url'],
                }
                github_repo, _ = GithubRepo.objects.update_or_create(
                    repo_id=repo['id'],
                    defaults=repo_fields
                )

                contributor_fields = {
                    'account': github_account,
                    'repo': github_repo
                }
                GithubRepoContributor.objects.update_or_create(
                    repo__repo_id=repo['id'],
                    account__username=username,
                    defaults=contributor_fields
                )

            if len(programming_languages) > 0: 
                github_account.programming_languages = repr(list(programming_languages))

            if len(technologies) > 0: 
                github_account.technologies = repr(list(technologies))

            github_account.save()

    return HttpResponse(f'GithubRepo objects: {GithubRepo.objects.count()}\nGithubRepoContributor objects: {GithubRepoContributor.objects.count()}')

def get_repos_with_common_contributors(request):
    common_repos = []
    counts = GithubRepo.objects.annotate(number_of_common_collaborators=Count('githubrepocontributor'))

    for count in counts:
        if count.number_of_common_collaborators > 1:
            common_repos.append(count.name)

    return HttpResponse(f'{common_repos}, {len(common_repos)}')


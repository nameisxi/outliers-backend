import json

from django.http import HttpResponse
from django.db.models import Count

from .models import *
from users.models import GithubAccount


def create_repos(request):
    with open('./repos/repos.json', 'r') as f:
        users_repos = json.load(f)

        for user_repos in users_repos:
            username = user_repos['username']
            github_account = GithubAccount.objects.get(username=username)

            for repo in user_repos['repos']:
                if repo['fork']: continue
                
                repo_fields = {
                    'repo_id': repo['id'],
                    'name': repo['name'],
                    'stargazers_count': repo['stargazers_count'],
                    'forks_count': repo['forks_count'], 
                    'watchers_count': repo['watchers_count'], 
                    'size_in_kilobytes': repo['size'], 
                    'repo_html_url': repo['html_url'],
                    'repo_api_url': repo['url'],
                }
                github_repo, _ = GithubRepo.objects.get_or_create(
                    repo_id=repo['id'],
                    defaults=repo_fields
                )

                if repo['language']:
                    repo_language = repo['language'].lower().strip()
                    programming_language, _ = GithubProgrammingLanguage.objects.get_or_create(name=repo_language)
                    github_repo.main_language.add(programming_language)

                if repo['topics']:
                    for technology in repo['topics']:
                        technology = technology.lower().strip()
                        topic, _ = GithubTopic.objects.get_or_create(name=technology)
                        github_repo.technologies_and_topics.add(topic)

                github_repo.save()

                contributor_fields = {
                    'account': github_account,
                    'repo': github_repo
                }
                GithubRepoContributor.objects.update_or_create(
                    repo__repo_id=repo['id'],
                    account__username=username,
                    defaults=contributor_fields
                )

    return HttpResponse(f'GithubRepo objects: {GithubRepo.objects.count()}\nGithubRepoContributor objects: {GithubRepoContributor.objects.count()}')

def get_repos_with_common_contributors(request):
    common_repos = []
    counts = GithubRepo.objects.annotate(number_of_common_collaborators=Count('githubrepocontributor'))

    for count in counts:
        if count.number_of_common_collaborators > 1:
            common_repos.append(count.name)

    return HttpResponse(f'{common_repos}, {len(common_repos)}')


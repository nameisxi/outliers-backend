
from technologies.models import ProgrammingLanguage, Topic
from ..models import *


class GithubRepoCreator:
    def __init__(self):
        pass

    def create_repos(self, repos):
        print('Creating GithubRepos...')

        tenth = round(len(repos) * 0.1)

        for i, user_repos in enumerate(repos):
            if (i + 1) % tenth == 0:
                print(f'    {((i + 1) / len(repos)) * 100}%')

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

        print('    - Done')
        print()

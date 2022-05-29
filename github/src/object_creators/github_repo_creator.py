from technologies.models import ProgrammingLanguage, Topic
from ...models import *


class GithubRepoCreator:
    def __init__(self, language_colors):
        self._language_colors = language_colors

    def _create_repo_object(self, repo):
        """
        Takes a dictionary object representing a Github repo from the Github REST API as an input and saves it into the database as a GithubRepo object or updates an already existing object. Created or updated object will be returned.
        """
        return GithubRepo.objects.update_or_create(
                    repo_id=repo['id'],
                    defaults={
                        'repo_created_at': repo['created_at'].split('T')[0],
                        'repo_updated_at': repo['updated_at'].split('T')[0],
                        'pushed_at': repo['pushed_at'],
                        'repo_id': repo['id'],
                        'name': repo['name'],
                        'stargazers_count': repo['stargazers_count'],
                        'normalized_stargazers_count': -1,
                        'forks_count': repo['forks_count'], 
                        'normalized_forks_count': -1,
                        'watchers_count': repo['watchers_count'], 
                        'normalized_watchers_count': -1,
                        'size_in_bytes': repo['size'], 
                        'normalized_size_in_bytes': -1,
                        'programming_languages_count': 0, 
                        'normalized_programming_languages_count': -1,
                        'repo_html_url': repo['html_url'],
                        'repo_api_url': repo['url'],
                    }
                )

    def _create_repo_language_object(self, repo, github_repo, github_account):
        """
        Creates a GithubRepoLanguage object and a GithubAccountLanguage object of a given repo language.
        """
        language = repo['language'].lower().strip()
        try:
            color = self._language_colors[language]['color']
        except Exception as e:
            color = '#ffffff'

        programming_language, _ = ProgrammingLanguage.objects.get_or_create(
            name=language, 
            defaults={
                'name': language,
                'color': color,
            }
        )
        
        GithubRepoLanguage.objects.update_or_create(
            repo=github_repo,
            language=programming_language, 
            defaults={
                'repo': github_repo,
                'language': programming_language,
                'language_share': -1.0,
                'language_contribution': -1,
            }
        )

        GithubAccountLanguage.objects.update_or_create(
            account=github_account,
            language=programming_language, 
            defaults={
                'account': github_account,
                'language': programming_language,
                'language_share': -1.0,
                'language_share_current_year': -1.0,
                'language_share_second_year': -1.0,
                'language_share_third_year': -1.0,
            }
        )

    def _create_repo_topic_objects(self, repo, github_repo, github_account):
        """
        Creates GithubRepoTopic objects and GithubAccountTopic objects of a given repos topics.
        """
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

    def create_repos(self, repos):
        """
        Creates GithubRepo objects of given Github-user/Github-repo pair from the Github REST API.
        """
        print('Creating GithubRepos...')

        tenth = max(round(len(repos) * 0.1), 1)

        for i, user_repos in enumerate(repos):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(repos)) * 100)}%')

            username = user_repos['username']
            github_account = GithubAccount.objects.get(username=username)

            for repo in user_repos['repos']:
                # Forks are not considered personal repos
                if repo['fork']: continue

                # Create a repo with given values, or update an existing one
                github_repo, _ = self._create_repo_object(repo)
                # Create a repo contributor with given values, or update an existing one
                github_account.repos.add(github_repo)
                # Add main programming language of the repo
                if repo['language']:
                    self._create_repo_language_object(repo, github_repo, github_account)
                # Add topics of the repo
                # TODO: add a check whether topic is really a topic or a technology, like Django
                if repo['topics']:
                    self._create_repo_topic_objects(repo, github_repo, github_account)

        print('    - Done')
        print()

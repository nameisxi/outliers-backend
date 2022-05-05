from technologies.models import ProgrammingLanguage
from ..models import *


class GithubMetadataCreator:
    def __init__(self):
        pass

    def _create_language_objects(self, repo, languages):
        """
        Creates GithubRepoLanguage and GithubAccountLanguage objects of a given repo and its programming languages.
        """
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

    def create_programming_languages(self, repos):
        """
        Gets a list of dictionary objects where each key represents a Github repo id and every value a list of programming languages from the Github REST API. This data will be used to create GithubRepoLanguage and GithubAccountLanguage objects that connect ProgrammingLanguage objects with GithubRepo objects and GithubAccount objects.
        """
        print('Creating GithubRepoLanguages & GithubAccountLanguages...')

        i = 1
        tenth = round(len(repos.keys()) * 0.1)

        for repo_id, languages in repos.items():
            if i % tenth == 0: print(f'    {(i / len(repos.keys())) * 100}%')
            i += 1
            
            try:
                repo = GithubRepo.objects.get(repo_id=repo_id)
            except GithubRepo.DoesNotExist:
                continue

            self._create_language_objects(repo, languages)
            
        print('    - Done')
        print()

    def calculate_programming_languages_counts(self):
        """
        Calculates how many programming languages each repo has and saves the value as a database field.
        """
        print('Calculating GithubRepoLanguage.programming_languages_counts...')

        repos = GithubRepo.objects.all()

        for repo in repos:
            repo.programming_languages_count = repo.programming_languages.all().count()
        
        GithubRepo.objects.bulk_update(repos, ['programming_languages_count'])

        print('    - Done')
        print()

    def calculate_programming_languages_shares(self):
        """
        Calculates programming languages' percentage share of every users codebase as a whole for every user who has used that language.
        """
        print('Calculating GithubAccountLanguage.language_shares...')

        account_languages = GithubAccountLanguage.objects.all()

        for account_language in account_languages:
            all_contributions = account_language.account.contributions.aggregate(models.Sum('repo__programming_languages__language_share'))['repo__programming_languages__language_share__sum']
            language_contributions = account_language.account.contributions.filter(repo__programming_languages__language=account_language.language).aggregate(models.Sum('repo__programming_languages__language_share'))['repo__programming_languages__language_share__sum']
            
            account_language.language_share = language_contributions / all_contributions
        
        GithubAccountLanguage.objects.bulk_update(account_languages, ['language_share'])

        print('    - Done')
        print()

    def calculate_topics_shares(self):
        """
        Calculates topics' percentage share of every users codebase as a whole for every user who has used that topic.
        """
        print('Calculating GithubAccountLanguage.topic_shares...')

        account_topics = GithubAccountTopic.objects.all()

        for account_topic in account_topics:
            repos_count = account_topic.account.repos_count
            if repos_count == 0: continue
            topic_count = account_topic.account.contributions.filter(repo__topics__topic=account_topic.topic).count()
            
            account_topic.topic_share = topic_count / repos_count
        
        GithubAccountTopic.objects.bulk_update(account_topics, ['topic_share'])        

        print('    - Done')
        print()

import json
from datetime import date

from technologies.models import ProgrammingLanguage
from ...models import *


class GithubMetadataCreator:
    def __init__(self):
        pass

    def _create_language_objects(self, repo, languages, language_colors):
        """
        Creates GithubRepoLanguage and GithubAccountLanguage objects of a given repo and its programming languages.
        """
        total_contributions_count = sum(list(languages.values()))
        if total_contributions_count == 0:
            return

        for language, language_contributions_count in languages.items():
            # TODO: if language_contribution_count, e.g. contribution filesize, < x, skip?
            if language_contributions_count == 0:
                continue

            language = language.lower().strip()
            try:
                color = language_colors[language]['color']
            except Exception as e:
                color = '#ffffff'

            programming_language, _ = ProgrammingLanguage.objects.update_or_create(
                                                                    name=language, 
                                                                    defaults={
                                                                        'name': language,
                                                                        'color': color,
                                                                    }
                                                                )

            # Add programming language relationship with each repo
            GithubRepoLanguage.objects.update_or_create(
                repo=repo,
                language=programming_language, 
                defaults={
                    'repo': repo,
                    'language': programming_language,
                    'language_share': language_contributions_count / total_contributions_count,
                    'language_contribution': language_contributions_count,
                }
            )

            # Add programming language relationship with each account
            for collaborator in repo.collaborators.all():
                GithubAccountLanguage.objects.update_or_create(
                    account=collaborator,
                    language=programming_language, 
                    defaults={
                        'account': collaborator,
                        'language': programming_language,
                        'language_share': -1.0,
                        'language_share_current_year': -1.0,
                        'language_share_second_year': -1.0,
                        'language_share_third_year': -1.0,
                    }
                )  

        # for repo_languages_object in languages:
        #     total_contributions_count = sum(list(repo_languages_object.values()))
        #     if total_contributions_count == 0:
        #         continue

        #     for language, language_contributions_count in repo_languages_object.items():
        #         # TODO: if language_contribution_count, e.g. contribution filesize, < x, skip?
        #         if language_contributions_count == 0:
        #             continue

        #         language = language.lower().strip()
        #         try:
        #             color = language_colors[language]['color']
        #         except Exception as e:
        #             color = '#ffffff'

        #         programming_language, _ = ProgrammingLanguage.objects.update_or_create(
        #                                                                             name=language, 
        #                                                                             defaults={
        #                                                                                 'name': language,
        #                                                                                 'color': color,
        #                                                                             }
        #                                                                         )

        #         # Add programming language relationship with each repo
        #         GithubRepoLanguage.objects.update_or_create(
        #             repo=repo,
        #             language=programming_language, 
        #             defaults={
        #                 'repo': repo,
        #                 'language': programming_language,
        #                 'language_share': language_contributions_count / total_contributions_count,
        #                 'language_contribution': language_contributions_count,
        #             }
        #         )

        #         # Add programming language relationship with each account
        #         for collaborator in repo.collaborators.all():
        #             GithubAccountLanguage.objects.update_or_create(
        #                 account=collaborator,
        #                 language=programming_language, 
        #                 defaults={
        #                     'account': collaborator,
        #                     'language': programming_language,
        #                     'language_share': -1.0,
        #                     'language_share_current_year': -1.0,
        #                     'language_share_second_year': -1.0,
        #                     'language_share_third_year': -1.0,
        #                 }
        #             )  

    def create_programming_languages(self, repos, language_colors):
        """
        Gets a list of dictionary objects where each key represents a Github repo id and every value a list of programming languages from the Github REST API. This data will be used to create GithubRepoLanguage and GithubAccountLanguage objects that connect ProgrammingLanguage objects with GithubRepo objects and GithubAccount objects.
        """
        print('Creating GithubRepoLanguages & GithubAccountLanguages...')

        i = 1
        tenth = max(round(len(repos.keys()) * 0.1), 1)

        for repo_id, languages in repos.items():
            if i % tenth == 0: print(f'    {round((i / len(repos.keys())) * 100)}%')
            i += 1
            
            try:
                repo = GithubRepo.objects.get(repo_id=repo_id)
            except GithubRepo.DoesNotExist:
                continue

            self._create_language_objects(repo, languages['languages'], language_colors)
            
        print('    - Done')
        print()

    def calculate_programming_languages_counts(self):
        """
        Calculates how many programming languages each repo has and saves the value as a database field.
        """
        print('Calculating GithubRepoLanguage.programming_languages_counts...')

        repos = GithubRepo.objects.all()

        for repo in repos:
            repo.programming_languages_count = repo.programming_languages.count()
        
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
            if account_language.account.repos.count() == 0:
                continue

            all_contributions = account_language.account.repos.aggregate(models.Sum('programming_languages__language_contribution'))['programming_languages__language_contribution__sum']
            language_contributions = account_language.account.repos.filter(programming_languages__language=account_language.language).aggregate(models.Sum('programming_languages__language_contribution'))['programming_languages__language_contribution__sum']
            account_language.language_share = language_contributions / all_contributions
        
        GithubAccountLanguage.objects.bulk_update(account_languages, ['language_share'])

        print('    - Done')
        print()

    def calculate_programming_languages_yearly_shares(self):
        """
        Calculates programming languages' yearly percentage share of users active repo during that year.
        """

        current_year = date.today().year
        years = [current_year - i for i in range(3)]
        years.reverse()

        year_to_field_name = {
            years[2]: 'language_share_current_year',
            years[1]: 'language_share_second_year',
            years[0]: 'language_share_third_year',
        }

        active_repo_counts = {
            years[2]: {},
            years[1]: {},
            years[0]: {},
        }

        account_languages = GithubAccountLanguage.objects.all()

        for year in years:
            print(f'Calculating GithubAccountLanguage.{year_to_field_name[year]}...')

            for account_language in account_languages:
                if account_language.account.repos.count() == 0:
                    continue

                account_id = account_language.account.id

                if active_repo_counts[year].get(account_id) is None:
                    active_repo_counts[year][account_id] = account_language.account.repos.filter(
                                                                                            repo_created_at__year__lte=year, 
                                                                                            pushed_at__year__gte=year,
                                                                                        ).count()
                
                if active_repo_counts[year][account_id] == 0:
                    setattr(account_language, year_to_field_name[year], 0)
                    continue

                active_language_repo_counts = account_language.account.repos.filter(
                                                                                repo_created_at__year__lte=year, 
                                                                                pushed_at__year__gte=year, 
                                                                                programming_languages__language=account_language.language
                                                                            ).count()

                yearly_share = active_language_repo_counts / active_repo_counts[year][account_id]
                setattr(account_language, year_to_field_name[year], yearly_share)
        
        GithubAccountLanguage.objects.bulk_update(account_languages, list(year_to_field_name.values()))

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
            topic_count = account_topic.account.repos.filter(topics__topic=account_topic.topic).count()

            account_topic.topic_share = topic_count / repos_count
        
        GithubAccountTopic.objects.bulk_update(account_topics, ['topic_share'])        

        print('    - Done')
        print()

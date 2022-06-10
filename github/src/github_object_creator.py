import os
import json

from .github_data_reader import GithubDataReader
from .object_creators import GithubAccountCreator
from .object_creators import GithubRepoCreator
from .object_creators import GithubMetadataCreator


class GithubObjectCreator:
    def __init__(self):
        self._data_reader = GithubDataReader()

        language_colors = self._data_reader.read_github_programming_language_color_data()
        # language_colors = {}
        # with open(f'./github/data/language_colors/github_language_colors.json', 'r', encoding='utf-8') as f:
        #     language_colors = json.load(f)
        #     language_colors = {k.lower(): v for k, v in language_colors.items()}

        self._github_account_creator = GithubAccountCreator()
        self._github_repo_creator = GithubRepoCreator(language_colors)
        self._github_metadata_creator = GithubMetadataCreator()

    # def _get_newest_files_path(self, directory_path, file_type):
    #     """
    #     Finds the newest (assumes timestamp in the filename) file's path in a given directory.
    #     """
    #     directory_files = os.listdir(directory_path)
    #     directory_files = [filename for filename in directory_files if file_type in filename]
    #     directory_files.sort(reverse=True)

    #     if len(directory_files) > 0:
    #         file_path = f'{directory_path}{directory_files[0]}'
    #         return file_path

    #     return None

    def create_github_accounts(self):
        """
        Opens a JSON file containing Github user accounts from Github REST API. The data will get passed to GithubAccountCreator that saves the data into the database.
        """
        # directory_path = './github/data/accounts/'
        # file_type = '.json'
        # file_path = self._get_newest_files_path(directory_path, file_type)

        # if not file_path:
        #     print(f'[!] No files found in {directory_path}. Aborting GithubAccounts creation.')
        #     return 

        # print(f'Using the following file: {file_path.split("/")[-1]}')

        # with open(file_path, 'r') as f:
        #     users = json.load(f)

        accounts, data_scraped_at = self._data_reader.read_github_account_data()
        self._github_account_creator.create_accounts(accounts, data_scraped_at)

    def create_github_organizations(self):
        """
        Opens a JSON file containing Github account ids and the organizations those accounts belong to from Github REST API. The data will get passed to GithubMetadataCreator that saves the data into the database.
        """
        # directory_path = './github/data/organizations/'
        # file_type = '.json'
        # file_path = self._get_newest_files_path(directory_path, file_type)

        # if not file_path:
        #     print(f'[!] No files found in {directory_path}. Aborting GithubOrganizations creation.')
        #     return 

        # print(f'Using the following file: {file_path.split("/")[-1]}')

        # with open(file_path, 'r') as f:
        #     organizations = json.load(f)

        organizations, data_scraped_at = self._data_reader.read_github_organization_data()
        self._github_metadata_creator.create_organizations(organizations, data_scraped_at)

    def create_github_contributions_calendars(self):
        # """
        # Opens a JSON file containing Github account ids and the contributions calendars of those accounts from Github Skyline API. The data will get passed to GithubMetadataCreator that saves the data into the database.
        # """
        # directory_path = './github/data/contributions/'
        # file_type = '.json'
        # file_path = self._get_newest_files_path(directory_path, file_type)

        # if not file_path:
        #     print(f'[!] No files found in {directory_path}. Aborting GithubContributionsCalendars creation.')
        #     return 

        # print(f'Using the following file: {file_path.split("/")[-1]}')

        # with open(file_path, 'r') as f:
        #     contributions_calendars = json.load(f)

        contribution_calendars, data_scraped_at = self._data_reader.read_github_contribution_calendar_data()
        self._github_metadata_creator.create_contributions_calendars(contribution_calendars, data_scraped_at)

    def create_github_repos(self):
        """
        Opens a JSON file containing Github repos from Github REST API. The data will get passed to GithubRepoCreator that saves the data into the database.
        """
        # directory_path = './github/data/repos/'
        # file_type = '.json'
        # file_path = self._get_newest_files_path(directory_path, file_type)

        # if not file_path:
        #     print(f'[!] No files found in {directory_path}. Aborting GithubRepos creation.')
        #     return 

        # print(f'Using the following file: {file_path.split("/")[-1]}')

        # with open(file_path, 'r') as f:
        #     repos = json.load(f)
        
        repos, data_scraped_at = self._data_reader.read_github_repo_data()
        self._github_repo_creator.create_repos(repos, data_scraped_at)

    def create_github_programming_languages(self):
        """
        Opens a JSON file containing list of repo IDs and those repos' programming languages from Github REST API. The data will get passed to GithubMetadataCreator that saves the data into the database.
        """
        # directory_path = './github/data/languages/'
        # file_type = '.json'
        # file_path = self._get_newest_files_path(directory_path, file_type)

        # if not file_path:
        #     print(f'[!] No files found in {directory_path}. Aborting GithubAccountLanguages and GithubRepoLanguages creation.')
        #     return 

        # print(f'Using the following file: {file_path.split("/")[-1]}')

        # language_colors = {}
        # with open(f'./github/data/language_colors/github_language_colors.json', 'r', encoding='utf-8') as f:
        #     language_colors = json.load(f)
        #     language_colors = {k.lower(): v for k, v in language_colors.items()}

        # with open(file_path, 'r') as f:
        #     repos = json.load(f)

        languages, data_scraped_at = self._data_reader.read_github_programming_language_data()
        language_colors = self._data_reader.read_github_programming_language_color_data()
        self._github_metadata_creator.create_programming_languages(languages, language_colors, data_scraped_at)

    def create_github_metadata(self):
        """
        Calls GithubMetadataCreator that generates metadata from GithubRepos and saves the metadata into the database.
        """
        # self._github_metadata_creator.calculate_programming_languages_counts()
        self._github_metadata_creator.calculate_programming_languages_shares()
        self._github_metadata_creator.calculate_programming_languages_yearly_shares()
        self._github_metadata_creator.calculate_topics_shares()

    def create(self):
        self.create_github_accounts()
        self.create_github_contributions_calendars()
        self.create_github_organizations()
        self.create_github_repos()
        self.create_github_programming_languages()
        self.create_github_metadata()

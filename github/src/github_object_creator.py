import os
import json

from .object_creators import GithubAccountCreator
from .object_creators import GithubRepoCreator
from .object_creators import GithubMetadataCreator


class GithubObjectCreator:
    def __init__(self):
        self._github_account_creator = GithubAccountCreator()
        self._github_repo_creator = GithubRepoCreator()
        self._github_metadata_creator = GithubMetadataCreator()

    def _get_newest_files_path(self, directory_path, file_type):
        """
        Finds the newest (assumes timestamp in the filename) file's path in a given directory.
        """
        directory_files = os.listdir(directory_path)
        directory_files = [filename for filename in directory_files if file_type in filename]
        directory_files.sort(reverse=True)

        if len(directory_files) > 0:
            file_path = f'{directory_path}{directory_files[0]}'
            return file_path

        return None

    def create_github_accounts(self):
        """
        Opens a JSON file containing Github user accounts from Github REST API. The data will get passed to GithubAccountCreator that saves the data into the database.
        """
        directory_path = './github/data/accounts/'
        file_type = '.json'
        file_path = self._get_newest_files_path(directory_path, file_type)

        if not file_path:
            print(f'[!] No files found in {directory_path}. Aborting GithubAccounts creation.')
            return 

        with open(file_path, 'r') as f:
            users = json.load(f)
            self._github_account_creator.create_accounts(users)

    def create_github_repos(self):
        """
        Opens a JSON file containing Github repos from Github REST API. The data will get passed to GithubRepoCreator that saves the data into the database.
        """
        directory_path = './github/data/repos/'
        file_type = '.json'
        file_path = self._get_newest_files_path(directory_path, file_type)

        if not file_path:
            print(f'[!] No files found in {directory_path}. Aborting GithubRepos creation.')
            return 

        with open(file_path, 'r') as f:
            repos = json.load(f)
            self._github_repo_creator.create_repos(repos)

    def create_github_programming_languages(self):
        """
        Opens a JSON file containing list of repo IDs and those repos' programming languages from Github REST API. The data will get passed to GithubMetadataCreator that saves the data into the database.
        """
        directory_path = './github/data/repo_languages/'
        file_type = '.json'
        file_path = self._get_newest_files_path(directory_path, file_type)

        if not file_path:
            print(f'[!] No files found in {directory_path}. Aborting GithubAccountLanguages and GithubRepoLanguages creation.')
            return 

        with open(file_path, 'r') as f:
            repos = json.load(f)
            self._github_metadata_creator.create_programming_languages(repos)

    def create_github_metadata(self):
        """
        Calls GithubMetadataCreator that generates metadata from GithubRepos and saves the metadata into the database.
        """
        self._github_metadata_creator.calculate_programming_languages_counts()
        self._github_metadata_creator.calculate_programming_languages_shares()
        self._github_metadata_creator.calculate_programming_languages_yearly_shares()
        self._github_metadata_creator.calculate_topics_shares()

    def create(self):
        self.create_github_accounts()
        self.create_github_repos()
        self.create_github_programming_languages()
        self.create_github_metadata()

import json

from .github_account_creator import GithubAccountCreator
from .github_repo_creator import GithubRepoCreator
from .github_metadata_creator import GithubMetadataCreator


class GithubPopulator:
    def __init__(self):
        self._github_account_creator = GithubAccountCreator()
        self._github_repo_creator = GithubRepoCreator()
        self._github_metadata_creator = GithubMetadataCreator()

    def create_github_accounts(self):
        """
        Opens a JSON file containing Github user accounts from Github REST API. The data will get passed to GithubAccountCreator that saves the data into the database.
        """
        with open('./github/data/users/users_v3.json', 'r') as f:
            users = json.load(f)
            self._github_account_creator.create_accounts(users)

    def create_github_repos(self):
        """
        Opens a JSON file containing Github repos from Github REST API. The data will get passed to GithubRepoCreator that saves the data into the database.
        """
        with open('./github/data/repos/repos_v3.json', 'r') as f:
            repos = json.load(f)
            self._github_repo_creator.create_repos(repos)

    def create_github_programming_languages(self):
        """
        Opens a JSON file containing list of repo IDs and those repos' programming languages from Github REST API. The data will get passed to GithubMetadataCreator that saves the data into the database.
        """
        with open('./github/data/languages/languages_v2.json', 'r') as f:
            repos = json.load(f)
            self._github_metadata_creator.create_programming_languages(repos)

    def create_github_metadata(self):
        """
        Calls GithubMetadataCreator that generates metadata from GithubRepos and saves the metadata into the database.
        """
        self._github_metadata_creator.calculate_programming_languages_counts()
        self._github_metadata_creator.calculate_programming_languages_shares()
        self._github_metadata_creator.calculate_topics_shares()


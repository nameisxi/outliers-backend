import os
import json
from datetime import datetime

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware


class GithubDataReader:
    def __init__(self):
        pass

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

    def _get_aware_date(self, date_str):
        date = parse_datetime(date_str)
        if not is_aware(date):
            date = make_aware(date)
        return date

    def _get_filename_timestamp(self, file_path):
        filename = file_path.split('/')[-1]
        data_scraped_at = filename.split('_')[-1].split('.')[0]
        try:
            data_scraped_at = self._get_aware_date(data_scraped_at)
        except Exception as e:
            print("Error while trying to parse filename timestamp:")
            print(e)
            print()
            data_scraped_at = datetime.strptime(data_scraped_at, '%Y-%m-%d')

        return data_scraped_at

    def read_github_account_data(self):
        """
        Opens a JSON file containing Github user accounts from Github REST API and return it.
        """
        directory_path = './github/data/accounts/'
        file_type = '.json'
        file_path = self._get_newest_files_path(directory_path, file_type)

        if not file_path:
            print(f'[!] No files found in {directory_path}. Aborting GithubAccounts creation.')
            return 

        print(f'Using the following file: {file_path.split("/")[-1]}')

        accounts = {}
        with open(file_path, 'r') as f:
            accounts = json.load(f)

        # if include_db_accounts:
        #     used_account_ids = set([account.id for account in accounts])
        #     for account in GithubAccount.objects.exclude(user_id__in=used_account_ids):
        #         accounts.append({
        #             'id': account.user_id,
        #             'login': account.username,
        #             'html_url': account.profile_html_url,
        #         })

        data_scraped_at = self._get_filename_timestamp(file_path)

        return accounts, data_scraped_at

    def read_github_organization_data(self):
        """
        Opens a JSON file containing Github account ids and the organizations those accounts belong to from Github REST API and return it.
        """
        directory_path = './github/data/organizations/'
        file_type = '.json'
        file_path = self._get_newest_files_path(directory_path, file_type)

        if not file_path:
            print(f'[!] No files found in {directory_path}. Aborting GithubOrganizations creation.')
            return 

        print(f'Using the following file: {file_path.split("/")[-1]}')

        organizations = {}
        with open(file_path, 'r') as f:
            organizations = json.load(f)

        data_scraped_at = self._get_filename_timestamp(file_path)
        
        return organizations, data_scraped_at

    def read_github_contribution_calendar_data(self):
        """
        Opens a JSON file containing Github account ids and the contributions calendars of those accounts from Github Skyline API and return it.
        """
        directory_path = './github/data/contributions/'
        file_type = '.json'
        file_path = self._get_newest_files_path(directory_path, file_type)

        if not file_path:
            print(f'[!] No files found in {directory_path}. Aborting GithubContributionsCalendars creation.')
            return 

        print(f'Using the following file: {file_path.split("/")[-1]}')

        contribution_calendars = {}
        with open(file_path, 'r') as f:
            contribution_calendars = json.load(f)

        data_scraped_at = self._get_filename_timestamp(file_path)
        
        return contribution_calendars, data_scraped_at

    def read_github_repo_data(self):
        """
        Opens a JSON file containing Github repos from Github REST API and return it.
        """
        directory_path = './github/data/repos/'
        file_type = '.json'
        file_path = self._get_newest_files_path(directory_path, file_type)

        if not file_path:
            print(f'[!] No files found in {directory_path}. Aborting GithubRepos creation.')
            return 

        print(f'Using the following file: {file_path.split("/")[-1]}')

        repos = {}
        with open(file_path, 'r') as f:
            repos = json.load(f)

        data_scraped_at = self._get_filename_timestamp(file_path)
        
        return repos, data_scraped_at

    def read_github_programming_language_data(self):
        """
        Opens a JSON file containing list of repo IDs and those repos' programming languages from Github REST API and return it.
        """
        directory_path = './github/data/languages/'
        file_type = '.json'
        file_path = self._get_newest_files_path(directory_path, file_type)

        if not file_path:
            print(f'[!] No files found in {directory_path}. Aborting GithubAccountLanguages and GithubRepoLanguages creation.')
            return 

        print(f'Using the following file: {file_path.split("/")[-1]}')

        repo_languages = {}
        with open(file_path, 'r') as f:
            repo_languages = json.load(f)

        data_scraped_at = self._get_filename_timestamp(file_path)

        return repo_languages, data_scraped_at

    def read_github_programming_language_color_data(self):
        language_colors = {}
        with open(f'./github/data/language_colors/github_language_colors.json', 'r', encoding='utf-8') as f:
            language_colors = json.load(f)
            language_colors = {k.lower(): v for k, v in language_colors.items()}

        return language_colors

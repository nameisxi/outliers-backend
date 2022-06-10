import json
from datetime import datetime

import pandas as pd
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware


class GithubDataWriter:
    def __init__(self):
        pass

    def _get_aware_date(self, date_str):
        date = parse_datetime(date_str)
        if not is_aware(date):
            date = make_aware(date)
        return date
            
    def write_account_urls(self, urls):
        current_time = datetime.now().isoformat()
        df = pd.DataFrame(data=urls.items(), columns=['account_url', 'contributions_count'])
        df.to_csv(f'./github/data/account_urls/github_account_urls_{current_time}.csv', index=False)

    def write_accounts_data(self, accounts):
        current_time = datetime.now().isoformat()
        with open(f'./github/data/accounts/github_accounts_{current_time}.json', 'w+', encoding='utf-8') as f:
            json.dump(accounts, f, ensure_ascii=False, indent=4)

    def write_repos_data(self, repos):
        current_time = datetime.now().isoformat()
        with open(f'./github/data/repos/github_repos_{current_time}.json', 'w+', encoding='utf-8') as f:
            json.dump(repos, f, ensure_ascii=False, indent=4)

    def write_accounts_contribution_data(self, contributions):
        current_time = datetime.now().isoformat()
        with open(f'./github/data/contributions/github_contributions_{current_time}.json', 'w+', encoding='utf-8') as f:
            json.dump(contributions, f, ensure_ascii=False, indent=4)
        
    def write_accounts_organization_data(self, organizations):
        current_time = datetime.now().isoformat()
        with open(f'./github/data/organizations/github_organizations_{current_time}.json', 'w+', encoding='utf-8') as f:
            json.dump(organizations, f, ensure_ascii=False, indent=4)

    def write_repos_language_data(self, repos_languages):
        current_time = datetime.now().isoformat()
        with open(f'./github/data/languages/github_repos_languages_{current_time}.json', 'w+', encoding='utf-8') as f:
            file_data = {}    
            file_data.update(repos_languages)
            json.dump(repos_languages, f, ensure_ascii=False, indent=4)
            
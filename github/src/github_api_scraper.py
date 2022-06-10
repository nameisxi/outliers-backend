import os, json
import time
from datetime import datetime

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

import requests
import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ghapi.all import GhApi
from fastcore.xtras import obj2dict

from ..models import GithubAccount, GithubRepo
from .github_data_writer import GithubDataWriter
from .github_data_reader import GithubDataReader


class GithubAPIScraper:
    def __init__(self):
        load_dotenv()
        self._api = GhApi(token=os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'))
        self._api_calls_remaining = None
        self._api_rate_limit_reset = None
        self._get_ratelimit()
        
        self._writer = GithubDataWriter()
        self._reader = GithubDataReader()

    def _get_aware_date(self, date_str):
        date = parse_datetime(date_str)
        if not is_aware(date):
            date = make_aware(date)
        return date
        
    def _get_ratelimit(self):
        rate_limit = self._api.rate_limit.get()['rate']
        self._api_calls_remaining = rate_limit['remaining']
        self._api_rate_limit_reset = self._get_aware_date(str(datetime.fromtimestamp(rate_limit['reset'])))
        
    def _sleep_until_rate_limit_reset(self):
        # Update the rate limit reset time just in case.
        self._get_ratelimit()
        
        # delta = self._api_rate_limit_reset - timezone.now()
        delta = self._api_rate_limit_reset - timezone.now()
        # Adding the extra 5 seconds just in case it takes the Github API some time to update the rate limit data.
        seconds_until_reset = delta.total_seconds() + 5
        
        if seconds_until_reset > 0:
            print()
            print(f'[!] Sleeping until API rate limit reset at {self._api_rate_limit_reset}')
            time.sleep(seconds_until_reset)
            print(' - Back to work')
            print()
        
        # Update the rate limit remaining count and next reset time since they have been reset.
        self._get_ratelimit()
    
    def _scrape_account_urls(self):
        print('Scraping account urls...')
        
        account_urls = {}
        url = 'https://raw.githubusercontent.com/gayanvoice/top-github-users/main/markdown/total_contributions/south_korea.md'
        result = requests.get(url)
        html = markdown.markdown(result.text)
        soup = BeautifulSoup(html, 'html.parser')
        urls = soup.find_all('a')

        tenth = max(round(len(urls) * 0.1), 1)

        for i, url in enumerate(urls):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(urls)) * 100)}% [{timezone.now()}]')
            
            if 'github.com' in url.get('href'):
                for child in url.findChildren():
                    if 'Avatar of' in child.get('alt'):
                        parent_td_tag = url.parent
                        contributions_td_tag = parent_td_tag.find_next_siblings('td')[4]
                        account_urls[url.get('href')] = int(contributions_td_tag.text)
                        break

        print(' - Done')
        print()
                        
        return account_urls
    
    def _scrape_accounts_data(self, urls):
        print('Scraping accounts...')
        self._get_ratelimit()
        
        accounts_data = []
        tenth = max(round(len(urls.keys()) * 0.1), 1)
        i = 0
    
        for url, contributions_count in urls.items():
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(urls.keys())) * 100)}% [{timezone.now()}]')
            i += 1
            
            if self._api_calls_remaining < 1:
                self._sleep_until_rate_limit_reset()
                    
            username = url.split('https://github.com/')[1].lower().strip()
            
            try:
                self._api_calls_remaining = self._api_calls_remaining - 1
                account_data = self._api.users.get_by_username(username)
                account_data = obj2dict(account_data)
                account_data['contributions_count'] = contributions_count
            except Exception as e:
                print()
                print(f"When handling account {username} at {url}")
                print("Error occurred:", e)
                print("Moving on...")
                print()
                
                # Some results, such as HTTP 404 don't count towards the Github REST API's rate limit,
                # where as some do, so we want to update the self._api_calls_remaining count.
                self._get_ratelimit()
                continue

            accounts_data.append(account_data)
            
        print(' - Done')
        print()

        return accounts_data
    
    def _scrape_repo_data(self, accounts):
        print('Scraping repos...')
        self._get_ratelimit()
        
        repos = []
        current_time = timezone.now()
        tenth = max(round(len(accounts) * 0.1), 1)

        for i, account in enumerate(accounts):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(accounts)) * 100)}% [{timezone.now()}]')
                
            if self._api_calls_remaining < 1:
                self._sleep_until_rate_limit_reset()

            try:
                # account_object = GithubAccount.objects.get(user_id=account['id'])
                # last_scraped = account_object.repos_scraped_at
                last_scraped = account.repos_scraped_at

                if last_scraped and (timezone.now() - last_scraped).days <= 7:
                    # print(f'    Skipping repos for GithubAccount(id={account["id"]}): last_scraped: {(timezone.now() - last_scraped).days} days ago')
                    print(f'    Skipping repos for GithubAccount(user_id={account.user_id}): last_scraped: {(timezone.now() - last_scraped).days} days ago')
                    continue
            except GithubAccount.DoesNotExist:
                pass

            # username = account['login']
            
            try:
                self._api_calls_remaining = self._api_calls_remaining - 1
                # TODO: paginate until pushed at or created at > 3y ago. 
                repos_data = self._api.repos.list_for_user(account.username, 'all', 'pushed', 'desc', 100, 1)
            except Exception as e:
                print()
                print(f"When handling account {account.username} at {account.profile_html_url}")
                print("Error occurred:", e)
                print("Moving on...")
                print()
                
                # Some results, such as HTTP 404 don't count towards the Github REST API's rate limit,
                # where as some do, so we want to update the self._api_calls_remaining count.
                self._get_ratelimit()
                continue
                        

            parsed_repos_data = []
            for repo_data in repos_data:
                parsed_repo_data = obj2dict(repo_data)

                # If repo is a fork, skip it.
                if parsed_repo_data['fork']: 
                    continue

                # If no commits have been made to this repo, no pushed_at value exists.
                if not parsed_repo_data['pushed_at']: 
                    continue

                # created_at_timestamp = parsed_repo_data['created_at'].split('T')[0]
                # created_at_time = datetime.strptime(created_at_timestamp, '%Y-%m-%d')
                created_at_time = self._get_aware_date(parsed_repo_data['created_at'])
                delta_between_creation = current_time - created_at_time

                # pushed_at_timestamp = parsed_repo_data['pushed_at'].split('T')[0]
                # pushed_at_time = datetime.strptime(pushed_at_timestamp, '%Y-%m-%d')
                pushed_at_time = self._get_aware_date(parsed_repo_data['pushed_at'])
                delta_between_last_push = current_time - pushed_at_time
                
                # Only repos that have been created within the last 3 years or pushed to within the last year will be counted
                if delta_between_creation.days <= (365 * 3) or delta_between_last_push.days <= (365 * 3):
                    parsed_repos_data.append(parsed_repo_data)

            repo = {
                'username': account.username,
                'repos': parsed_repos_data
            }
            repos.append(repo)
        
        print(' - Done')
        print()
        
        return repos

    def _scrape_accounts_organization_data(self, accounts):
        print('Scraping accounts organizations...')
        self._get_ratelimit()

        account_organizations = {}
        tenth = max(round(len(accounts) * 0.1), 1)
        
        for i, account in enumerate(accounts):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(accounts)) * 100)}% [{timezone.now()}]')

            if self._api_calls_remaining < 1:
                self._sleep_until_rate_limit_reset()

            try:
                # account_object = GithubAccount.objects.get(user_id=account['id'])
                # last_scraped = account_object.organizations_scraped_at
                last_scraped = account.organizations_scraped_at

                if last_scraped and (timezone.now() - last_scraped).days <= 30:
                    # print(f'    Skipping organizations for GithubAccount(id={account["id"]}): last_scraped: {(timezone.now() - last_scraped).days} days ago')
                    print(f'    Skipping organizations for GithubAccount(user_id={account.user_id}): last_scraped: {(timezone.now() - last_scraped).days} days ago')
                    continue
            except GithubAccount.DoesNotExist:
                pass

            # username = account['login']

            try:
                self._api_calls_remaining = self._api_calls_remaining - 1
                orgs_data = self._api.orgs.list_for_user(account.username, 100, 1)
            except Exception as e:
                print()
                print(f"When handling account {account.username} at {account.profile_html_url}")
                print("Error occurred:", e)
                print("Moving on...")
                print()
                
                # Some results, such as HTTP 404 don't count towards the Github REST API's rate limit,
                # where as some do, so we want to update the self._api_calls_remaining count.
                self._get_ratelimit()
                continue

            parsed_orgs_data = [obj2dict(org_data) for org_data in orgs_data]
            account_organizations[account.username] = parsed_orgs_data
            
        return account_organizations
        

    def _scrape_accounts_contribution_data(self, accounts):
        print('Scraping accounts contributions...')

        account_contributions = {}
        current_year = timezone.now().year
        years = [current_year - i for i in range(3)]
            
        tenth = max(round(len(accounts) * 0.1), 1)
        
        for i, account in enumerate(accounts):
            if (i + 1) % tenth == 0:
                    print(f'    {round(((i + 1) / len(accounts)) * 100)}% [{timezone.now()}]')
            
            try:
                # account_object = GithubAccount.objects.get(user_id=account['id'])
                # last_scraped = account_object.contributions_scraped_at
                last_scraped = account.contributions_scraped_at

                if last_scraped and (timezone.now() - last_scraped).days <= 7:
                    # print(f'    Skipping contributions for GithubAccount(id={account["id"]}): last_scraped: {(timezone.now() - last_scraped).days} days ago')
                    print(f'    Skipping contributions for GithubAccount(user_id={account.user_id}): last_scraped: {(timezone.now() - last_scraped).days} days ago')
                    continue

                # If this data has been previously scraped, only scrape the current year
                if last_scraped:
                    years = [timezone.now().year]
            except GithubAccount.DoesNotExist:
                pass
            
            account_contributions[account.username] = []
            
            for year in years:
                print(f'            {year} [{timezone.now()}]')
                try: 
                    url = f'https://skyline.github.com/{account.username}/{year}.json'
                    result = requests.get(url)
                    
                    account_contributions[account.username].append(json.loads(result.text))
                    
                except Exception as e:
                    print()
                    print(f"When handling account contributions at https://skyline.github.com/{account.username}/{year}.json")
                    print("Error occurred:", e)
                    print("Moving on...")
                    print()
                    continue
                    
            if (i + 1) % tenth == 0:
                self._writer.write_accounts_contribution_data(account_contributions)
                print('[!] Sleeping for 60 seconds...')
                time.sleep(60)
                print(' - Back to work')
                print()

        print(' - Done')
        print()
                        
        return account_contributions           
    
    def _scrape_repos_language_data(self, repos):
        print('Scraping repos languages...')
        self._get_ratelimit()
        
        repos_languages = {}
        tenth = max(round(len(repos) * 0.1), 1)

        # for i, repo_data in enumerate(repos):
        #     if (i + 1) % tenth == 0:
        #         print(f'    {round(((i + 1) / len(repos)) * 100)}% [{timezone.now()}]')

        #     for repo in repo_data['repos']:
        #         if not repo['language'] or repo['fork']:
        #             continue

        #         try:
        #             repo_object = GithubRepo.objects.get(repo_id=repo['id'])
        #             last_scraped = repo_object.languages_scraped_at

        #             pushed_at_timestamp = repo['pushed_at'].split('T')[0]
        #             last_pushed = datetime.strptime(pushed_at_timestamp, '%Y-%m-%d')

        #             if last_scraped and (timezone.now() - last_scraped).days <= 7 and last_pushed <= repo_object.updated_at:
        #                 print(f'    Skipping languages for GithubRepo(id={repo["id"]}): last_scraped: {(timezone.now() - last_scraped).days} days ago | last_pushed <= updated_at: {last_pushed <= repo_object.updated_at}')
        #                 continue
        #         except GithubRepo.DoesNotExist:
        #             pass

        #         repo_id = str(repo['id'])
        #         if repo_id not in repos_languages.keys():
        #             if self._api_calls_remaining < 1:
        #                 self._sleep_until_rate_limit_reset()
                        
        #             repos_languages[repo_id] = {
        #                 'owner': repo['owner'],
        #                 'html_url:': repo['html_url'],
        #                 'languages': {},
        #             }
                    
        #             try:
        #                 self._api_calls_remaining = self._api_calls_remaining - 1
        #                 languages = self._api.repos.list_languages(repo['owner']['login'], repo['name'])
        #                 languages = obj2dict(languages)
        #                 repos_languages[repo_id]['languages'] = languages
        #             except Exception as e:
        #                 print()
        #                 print(f"When handling repo {repo_id} at {repo['html_url']}")
        #                 print("Error occurred:", e)
        #                 print("Moving on...")
        #                 print()
                        
        #                 # Some results, such as HTTP 404 don't count towards the Github REST API's rate limit,
        #                 # where as some do, so we want to update the self._api_calls_remaining count.
        #                 self._get_ratelimit()
        #                 continue

        #             if len(repos_languages.keys()) % 1000 == 0:
        #                 self._writer.write_repos_language_data(repos_languages)
        
        for i, repo in enumerate(repos):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(repos)) * 100)}% [{timezone.now()}]')

            if repo.programming_languages.count() == 0:
                continue

            last_scraped = repo.languages_scraped_at

            if last_scraped and ((timezone.now() - last_scraped).days <= 7 or repo.pushed_at < last_scraped):
                print(f'    Skipping languages for GithubRepo(repo_id={repo.repo_id}): last_scraped: {(timezone.now() - last_scraped).days} days ago | last_pushed: {repo.pushed_at}')
                continue


            repo_id = str(repo.repo_id)
            if repo_id not in repos_languages.keys():
                if self._api_calls_remaining < 1:
                    self._sleep_until_rate_limit_reset()
                    
                repos_languages[repo_id] = {
                    'languages': {},
                }
                
                try:
                    self._api_calls_remaining = self._api_calls_remaining - 1
                    languages = self._api.repos.list_languages(repo.owner_username, repo.name)
                    languages = obj2dict(languages)
                    repos_languages[repo_id]['languages'] = languages
                except Exception as e:
                    print()
                    print(f"When handling repo {repo_id} at {repo.repo_html_url}")
                    print("Error occurred:", e)
                    print("Moving on...")
                    print()
                    
                    # Some results, such as HTTP 404 don't count towards the Github REST API's rate limit,
                    # where as some do, so we want to update the self._api_calls_remaining count.
                    self._get_ratelimit()
                    continue

                if len(repos_languages.keys()) % 1000 == 0:
                    self._writer.write_repos_language_data(repos_languages)
    

        print(' - Done')
        print()

        return repos_languages
    
    def scrape(self):
        # account_urls = self._scrape_account_urls()
        # self._writer.write_account_urls(account_urls)
        
        # accounts = self._scrape_accounts_data(account_urls)
        # self._writer.write_accounts_data(accounts)

        # organizations = self._scrape_accounts_organization_data(accounts)
        # self._writer.write_accounts_organization_data(organizations)

        # contributions = self._scrape_accounts_contribution_data(accounts)
        # self._writer.write_accounts_contribution_data(contributions)
        
        # repos = self._scrape_repo_data(accounts)
        # self._writer.write_repos_data(repos)
        
        # languages = self._scrape_repos_language_data(repos)
        # self._writer.write_repos_language_data(languages)

        # TODO: update to also include existing accounts from the db, etc.
        self.scrape_repos()
        self.scrape_languages()
        self.scrape_organizations()
        self.scrape_contributions()

    def scrape_accounts(self):
        account_urls = self._scrape_account_urls()
        self._writer.write_account_urls(account_urls)
        # accounts = self._scrape_accounts_data(account_urls)
        # self._writer.write_accounts_data(accounts)
        
    def scrape_repos(self):
        # accounts = self._reader.read_github_account_data(include_db_accounts=True)
        accounts = GithubAccount.objects.all()
        repos = self._scrape_repo_data(accounts)
        self._writer.write_repos_data(repos)

    def scrape_organizations(self):
        # accounts = self._reader.read_github_account_data(include_db_accounts=True)
        accounts = GithubAccount.objects.all()
        organizations = self._scrape_accounts_organization_data(accounts)
        self._writer.write_accounts_organization_data(organizations)

    def scrape_contributions(self):
        # accounts = self._reader.read_github_account_data(include_db_accounts=True)
        accounts = GithubAccount.objects.all()
        contributions = self._scrape_accounts_contribution_data(accounts)
        self._writer.write_accounts_contribution_data(contributions)

    def scrape_languages(self):
        # repos = self._reader.read_github_repo_data(include_db_repos=True)
        repos = GithubRepo.objects.all()
        repos_languages = self._scrape_repos_language_data(repos)
        self._writer.write_repos_language_data(repos_languages)

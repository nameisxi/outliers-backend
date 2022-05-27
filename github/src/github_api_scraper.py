import os, json
import time
from datetime import datetime

import requests
import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ghapi.all import GhApi
from fastcore.xtras import obj2dict

from .github_api_writer import GithubAPIWriter


class GithubAPIScraper:
    def __init__(self):
        load_dotenv()
        self._api = GhApi(token=os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'))
        self._api_calls_remaining = None
        self._api_rate_limit_reset = None
        self._get_ratelimit()
        
        self._writer = GithubAPIWriter()
        
    def _get_ratelimit(self):
        rate_limit = self._api.rate_limit.get()['rate']
        self._api_calls_remaining = rate_limit['remaining']
        self._api_rate_limit_reset = datetime.fromtimestamp(rate_limit['reset'])
        
    def _sleep_until_rate_limit_reset(self):
        # Update the rate limit reset time just in case.
        self._get_ratelimit()
        
        delta = self._api_rate_limit_reset - datetime.now()
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
                print(f'    {round(((i + 1) / len(urls)) * 100)}% [{datetime.now()}]')
            
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
                print(f'    {round(((i + 1) / len(urls.keys())) * 100)}% [{datetime.now()}]')
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
    
    def _scrape_repos_data(self, accounts):
        print('Scraping repos...')
        self._get_ratelimit()
        
        repos = []
        current_time = datetime.now()
        tenth = max(round(len(accounts) * 0.1), 1)

        for i, account in enumerate(accounts):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(accounts)) * 100)}% [{datetime.now()}]')
                
            if self._api_calls_remaining < 1:
                self._sleep_until_rate_limit_reset()
                    
            username = account['login']
            
            try:
                self._api_calls_remaining = self._api_calls_remaining - 1
                repos_data = self._api.repos.list_for_user(username, 'all', 'pushed', 'desc', 100, 1)
            except Exception as e:
                print()
                print(f"When handling account {username} at {account['html_url']}")
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

                if not parsed_repo_data['pushed_at']: 
                    continue

                created_at_timestamp = parsed_repo_data['created_at'].split('T')[0]
                created_at_time = datetime.strptime(created_at_timestamp, '%Y-%m-%d')
                delta_between_creation = current_time - created_at_time

                pushed_at_timestamp = parsed_repo_data['pushed_at'].split('T')[0]
                pushed_at_time = datetime.strptime(pushed_at_timestamp, '%Y-%m-%d')
                delta_between_last_push = current_time - pushed_at_time
                
                # Only repos that have been created within the last 3 years or pushed to within the last year will be counted
                if delta_between_creation.days <= (365 * 3) or delta_between_last_push.days <= (365 * 3):
                    parsed_repos_data.append(parsed_repo_data)

            repo = {
                'username': username,
                'repos': parsed_repos_data
            }
            repos.append(repo)
        
        print(' - Done')
        print()
        
        return repos
    
    
    def _scrape_repos_language_data(self, repos):
        print('Scraping repos languages...')
        self._get_ratelimit()
        
        repos_languages = {}
        tenth = max(round(len(repos) * 0.1), 1)

        for i, repo_data in enumerate(repos):
            if (i + 1) % tenth == 0:
                print(f'    {round(((i + 1) / len(repos)) * 100)}% [{datetime.now()}]')

            for repo in repo_data['repos']:
                if not repo['language'] or repo['fork']:
                    continue

                repo_id = str(repo['id'])
                if repo_id not in repos_languages.keys():
                    if self._api_calls_remaining < 1:
                        self._sleep_until_rate_limit_reset()
                        
                    repos_languages[repo_id] = {
                        'owner': repo['owner'],
                        'html_url:': repo['html_url'],
                        'languages': {},
                    }
                    
                    try:
                        self._api_calls_remaining = self._api_calls_remaining - 1
                        languages = self._api.repos.list_languages(repo['owner']['login'], repo['name'])
                        languages = obj2dict(languages)
                        repos_languages[repo_id]['languages'] = languages
                    except Exception as e:
                        print()
                        print(f"When handling repo {repo_id} at {repo['html_url']}")
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
        account_urls = self._scrape_account_urls()
        self._writer.write_account_urls(account_urls)
        
        accounts = self._scrape_accounts_data(account_urls)
        self._writer.write_accounts_data(accounts)
        
        repos = self._scrape_repos_data(accounts)
        self._writer.write_repos_data(repos)
        
        repos_languages = self._scrape_repos_language_data(repos)
        self._writer.write_repos_language_data(repos_languages)

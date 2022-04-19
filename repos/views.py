import json

from django.http import HttpResponse
from django.db.models import Count

from .models import *
from users.models import Candidate, GithubAccount


def create_repos(request):
    with open('./repos/repos_v2.json', 'r') as f:
        users_repos = json.load(f)

        for user_repos in users_repos:
            username = user_repos['username']
            github_account = GithubAccount.objects.get(username=username)

            for repo in user_repos['repos']:
                if repo['fork']: continue
                
                repo_fields = {
                    'repo_id': repo['id'],
                    'name': repo['name'],
                    'stargazers_count': repo['stargazers_count'],
                    'forks_count': repo['forks_count'], 
                    'watchers_count': repo['watchers_count'], 
                    'size_in_kilobytes': repo['size'], 
                    'repo_html_url': repo['html_url'],
                    'repo_api_url': repo['url'],
                }
                github_repo, _ = GithubRepo.objects.get_or_create(
                    repo_id=repo['id'],
                    defaults=repo_fields
                )

                if repo['language']:
                    repo_language = repo['language'].lower().strip()
                    programming_language, _ = GithubProgrammingLanguage.objects.get_or_create(name=repo_language)
                    github_repo.main_language.add(programming_language)

                if repo['topics']:
                    for technology in repo['topics']:
                        technology = technology.lower().strip()
                        topic, _ = GithubTopic.objects.get_or_create(name=technology)
                        github_repo.technologies_and_topics.add(topic)

                github_repo.save()

                contributor_fields = {
                    'account': github_account,
                    'repo': github_repo
                }
                GithubRepoContributor.objects.update_or_create(
                    repo__repo_id=repo['id'],
                    account__username=username,
                    defaults=contributor_fields
                )

    return HttpResponse(f'GithubRepo objects: {GithubRepo.objects.count()}\nGithubRepoContributor objects: {GithubRepoContributor.objects.count()}')

def get_repos_with_common_contributors(request):
    common_repos = []
    counts = GithubRepo.objects.annotate(number_of_common_collaborators=Count('githubrepocontributor'))

    for count in counts:
        if count.number_of_common_collaborators > 1:
            common_repos.append(count.name)

    return HttpResponse(f'{common_repos}, {len(common_repos)}')

def normalize(value):
    return value

def average(list):
    return sum(list) / len(list)

def calculate_work_score(candidate):
    github_account = candidate.github_account

    # Scoring the amount of work done
    normalized_repos_count = normalize(github_account.repos_count)
    normalized_gists_count = normalize(github_account.gists_count)
    normalized_contributions_count = normalize(github_account.contributions_count)
    work_amount_score = normalized_repos_count + normalized_gists_count + normalized_contributions_count

    # Scoring the complexity of work done
    normalized_average_repo_loc = 0
    normalized_average_repo_filesize = normalize(average([c.size_in_kilobytes for c in github_account.contributions]))
    normalized_average_repo_collaborators_count = 0
    normalized_average_repo_language_count = 0
    work_complexity_score = normalized_average_repo_loc + normalized_average_repo_filesize + normalized_average_repo_collaborators_count + normalized_average_repo_language_count 

    # Scoring the impact of work done
    normalized_average_repo_stargazers_count = normalize(average([c.stargazers_count for c in github_account.contributions]))
    normalized_average_repo_forks_count = normalize(average([c.forks_count for c in github_account.contributions]))
    normalized_average_repo_watchers_count = normalize(average([c.watchers_count for c in github_account.contributions]))
    work_impact_score = normalized_average_repo_stargazers_count + normalized_average_repo_forks_count + normalized_average_repo_watchers_count

    # Scoring the quality of work done
    # TODO
    work_quality_score = 0

    work_score = work_amount_score + work_complexity_score + work_impact_score + work_quality_score

    return work_score

def calculate_popularity_score(candidate):
    github_account = candidate.github_account

    # Scoring the amount of popularity
    normalized_github_followers_count = normalize(github_account.followers_count)
    normalized_github_followers_and_following_difference = normalize(github_account.followers_count - github_account.following_count)
    normalized_github_stargazers_count = 0
    
    popularity_score = normalized_github_followers_count + normalized_github_followers_and_following_difference + normalized_github_stargazers_count

    return popularity_score

def calculate_company_ranking(company):
    return 1

def calculate_employee_satisfaction(company):
    return 1

def calculate_company_size(company):
    return 0

def calculate_company_average_salary(company, title=None):
    return 1

def calculate_company_average_tenure(company):
    return 1

def calculate_tenure(candidate):
    return 0

def calculate_hireability_score(candidate):
    # Scoring candidate's current employer
    employer = candidate.company
    normalized_company_ranking = 1 - normalize(calculate_company_ranking(employer)) # Smaller is better: top company employees are harder to hire
    normalized_employee_satisfaction = 1 - normalize(calculate_employee_satisfaction(employer)) # Smaller is better: unhappy employees are easier to hire
    normalized_average_company_salary = 1 - normalize(calculate_company_average_salary(employer)) # Smaller is better: underpaid employees are easier to hire
    normalized_average_company_tenure = 1 - normalize(calculate_company_average_tenure(employer)) # Smaller is better: high turnover == easier to hire
    current_employer_score = normalized_company_ranking + normalized_employee_satisfaction + normalized_average_company_salary + normalized_average_company_tenure

    # Scoring candidate's current position
    normalized_level_or_title = 0 # Smaller is better because there could always be a better title
    normalized_average_company_salary_for_position = 1 - normalize(calculate_company_average_salary(employer, title=candidate.title)) # Smaller is better because underpaid employees are easier to hire
    current_position_score = normalized_level_or_title + normalized_average_company_salary_for_position

    # Scoring candidate's willingness to change jobs
    normalized_candidate_tenure = normalize(calculate_tenure(candidate)) # Larger is better: the longer someone has stayed, the more likely they will consider looking elsewhere
    normalized_tenure_difference = normalize(normalized_candidate_tenure - normalized_average_company_tenure) # Larger is better: candidate has been at the company longer than an average employee
    github_hireable = 0
    if candidate.github_account.hireable is not None and candidate.github_account.hireable:
        github_hireable = 1
    linkedin_open_for_work = 0
    willlingness_to_change_jobs_score = normalized_candidate_tenure + normalized_tenure_difference + github_hireable + linkedin_open_for_work

    hireability_score = current_employer_score + current_position_score + willlingness_to_change_jobs_score

    return hireability_score


def calculate_fit_score(candidate):
    # basically stuff like job opening vs candidate's current job
    # normalized_employee_count_difference = 1 - normalize(abs(Company.employee_count - calculate_company_size(employer))) # Smaller is better: the less the employee counts differ, the more likely the company size wont be an issue to a candidate 
    # normalized_level_or_title_difference = normalize(calculate_title_value(Opening.title) - calculate_title_value(candidate.title)) # Larger is better: the smaller the candidates title compared to the openings title, the easier they are to hire
    pass


def compute_ranking_scores(request):
    for candidate in Candidate.objects.all():        
        candidate.work_score = calculate_work_score(candidate)
        candidate.popularity_score = calculate_popularity_score(candidate)
        candidate.hireability_score = calculate_hireability_score(candidate)
        # candidate.fit_score = calculate_fit_score(candidate)
        candidate.save()



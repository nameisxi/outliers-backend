

class WorkScorer:
    def __init__(self):
        pass

    def _average(self, list):
        """
        Calculates a mathematical average for a given list.
        """
        print()
        print()
        print()
        print()
        print()
        print("LIST:", list)
        print()
        print()
        print()
        print()
        print()
        return sum(list) / len(list)

    def _calculate_work_quantity_score(self, github_account):
        """
        Scores a given candidate's Github profile based on the quantity, or the amount, of their previous work.
        """
        # normalized_contributions_count = github_account.normalized_contributions_count
        # normalized_repos_count = github_account.normalized_repos_count
        # TODO: normalized_codebase_size 
        work_quantity_score = [
            github_account.normalized_contributions_count,
            github_account.normalized_repos_count,
            github_account.normalized_codebase_size,
            github_account.normalized_language_count,
            # github_account.normalized_topic_count,   
        ]

        return work_quantity_score

    def _calculate_work_complexity_score(self, github_account):
        """
        Scores a given candidate's Github profile based on the complexity of their previous work.
        """
        # TODO: handle repos.count() == 0 better?
        # if github_account.repos.count() == 0:
        #     return [0]
            
        # normalized_average_repo_filesize = self._average([repo.normalized_size_in_bytes for repo in github_account.repos.all()])
        # normalized_average_repo_collaborators_count = 0
        # normalized_average_repo_language_count = self._average([c.repo.normalized_programming_languages_count for c in github_account.contributions.all()])

        # work_complexity_score = [normalized_average_repo_filesize]
        work_complexity_score = [
            github_account.normalized_average_codebase_size,
            github_account.normalized_average_language_count,
        ]

        return work_complexity_score

    def _calculate_work_impact_score(self, github_account):
        """
        Scores a given candidate's Github profile based on the impact of their previous work.
        """
        # if github_account.repos.count() == 0:
        #     return [0]

        # normalized_average_repo_stargazers_count = self._average([repo.normalized_stargazers_count for repo in github_account.repos.all()])
        # normalized_average_repo_forks_count = self._average([repo.normalized_forks_count for repo in github_account.repos.all()])
        # normalized_average_repo_watchers_count = self._average([repo.normalized_watchers_count for repo in github_account.repos.all()])
        
        # work_impact_score = self._average([normalized_average_repo_stargazers_count, normalized_average_repo_forks_count, normalized_average_repo_watchers_count])
        # work_impact_score = [normalized_average_repo_stargazers_count, normalized_average_repo_forks_count, normalized_average_repo_watchers_count]

        work_impact_score = [
            github_account.normalized_stargazer_count,
            github_account.normalized_average_stargazer_count,
            github_account.normalized_fork_count,
            github_account.normalized_average_fork_count,
            # github_account.normalized_watcher_count,
            # github_account.normalized_average_watcher_count,
        ]

        return work_impact_score

    # def _calculate_work_quality_score(self, github_account):
    #     """
    #     Scores a given candidate's Github profile based on the quality of their previous work.
    #     """
    #     return 0

    def calculate_work_score(self, candidate):
        """
        Calculates a work score for a given Candidate object.
        """
        work_scores = []

        # TODO: remove possibility for multiple github accounts per candidate?
        for github_account in candidate.github_accounts.all():
            work_quantity_score = self._calculate_work_quantity_score(github_account)
            work_complexity_score = self._calculate_work_complexity_score(github_account)
            work_impact_score = self._calculate_work_impact_score(github_account)

            print("Work score quantity:", work_quantity_score)
            print("Work score complexirt:", work_complexity_score)
            print("Work score impact:", work_impact_score)

            work_scores.append(self._average(work_quantity_score + work_complexity_score + work_impact_score))

        # return self._average(work_scores)
        return sum(work_scores)

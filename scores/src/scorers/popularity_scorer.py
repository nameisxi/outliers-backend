

class PopularityScorer:
    def __init__(self):
        pass

    def _average(self, list):
        """
        Calculates a mathematical average for a given list.
        """
        return sum(list) / len(list)

    def _calculate_github_popularity_score(self, github_account):
        """
        Calculates a github popularity score for a given GithubAccount object.
        """
        normalized_github_followers_count = github_account.normalized_followers_count
        normalized_github_followers_following_counts_difference = github_account.normalized_followers_following_counts_difference
        normalized_github_stargazers_count = 0

        return self._average([normalized_github_followers_count, normalized_github_followers_following_counts_difference])

    def calculate_popularity_score(self, candidate):
        """
        Calculates a popularity score for a given Candidate object.
        """
        popularity_scores = []
        
        github_popularity_scores = []
        for github_account in candidate.github_accounts.all():
            github_popularity_score = self._calculate_github_popularity_score(github_account)
            github_popularity_scores.append(github_popularity_score)

        # TODO: Twitter, blogs, etc.?

        popularity_scores.append(self._average(github_popularity_scores))

        return self._average(popularity_scores)
        
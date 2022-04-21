

class HireabilityScorer:
    def __init__(self):
        pass

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

    def _calculate_current_employer_score(self, candidate):
        employer = candidate.employer

        # normalized_company_ranking = 1 - calculate_company_ranking(employer) # Smaller is better: top company employees are harder to hire
        # normalized_employee_satisfaction = 1 - calculate_employee_satisfaction(employer) # Smaller is better: unhappy employees are easier to hire
        # normalized_average_company_salary = 1 - calculate_company_average_salary(employer) # Smaller is better: underpaid employees are easier to hire
        # normalized_average_company_tenure = 1 - calculate_company_average_tenure(employer) # Smaller is better: high turnover == easier to hire
        # current_employer_score = normalized_company_ranking + normalized_employee_satisfaction + normalized_average_company_salary + normalized_average_company_tenure
        return 0

    def _calculate_current_position_score(self, candidate):
        # normalized_level_or_title = 0 # Smaller is better because there could always be a better title
        # normalized_average_company_salary_for_position = 1 - normalize(calculate_company_average_salary(candidate.employer, title=candidate.title)) # Smaller is better because underpaid employees are easier to hire
        # current_position_score = normalized_level_or_title + normalized_average_company_salary_for_position

        return 0

    def _calculate_current_tenure_score(self, candidate):
        # normalized_candidate_tenure = calculate_tenure(candidate)) # Larger is better: the longer someone has stayed, the more likely they will consider looking elsewhere
        # normalized_tenure_difference = normalize(normalized_candidate_tenure - normalized_average_company_tenure) # Larger is better: candidate has been at the company longer than an average employee
        
        return 0

    def _calculate_open_to_jump_score(self, candidate):
        # github_hireable = 0
        # if candidate.github_accounts.hireable is not None and candidate.github_accounts.hireable:
        #     github_hireable = 1
        # linkedin_open_for_work = 0
        # willlingness_to_change_jobs_score = normalized_candidate_tenure + normalized_tenure_difference + github_hireable + linkedin_open_for_work

        return 0


    def calculate_hireability_score(self, candidate):
        # TODO: if jobless, return 1
        current_employer_score = self._calculate_current_employer_score(candidate)
        current_position_score = self._calculate_current_position_score(candidate)
        current_tenure_score = self._calculate_current_tenure_score(candidate)
        open_to_jump_score = self._calculate_open_to_jump_score(candidate)

        hireability_score = current_employer_score + current_position_score + current_tenure_score + open_to_jump_score

        return hireability_score


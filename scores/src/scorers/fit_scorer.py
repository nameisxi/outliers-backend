

class FitScorer:
    def __init__(self):
        pass

    def calculate_fit_score(self, candidate):
        # basically stuff like job opening vs candidate's current job
        # normalized_employee_count_difference = 1 - normalize(abs(Company.employee_count - calculate_company_size(employer))) # Smaller is better: the less the employee counts differ, the more likely the company size wont be an issue to a candidate 
        # normalized_level_or_title_difference = normalize(calculate_title_value(Opening.title) - calculate_title_value(candidate.title)) # Larger is better: the smaller the candidates title compared to the openings title, the easier they are to hire
        pass

import requests

class LeetCodeAPIClient:
    def __init__(self):
        self.base_url = "https://leetcode.com/api"

    def get_all_problems(self):
        """ Fetches all problems from the LeetCode API. """
        url = f"{self.base_url}/problems/all/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to retrieve problems from LeetCode API")

    def get_problem_by_id(self, problem_id):
        """ Fetches a specific problem by its ID. """
        problems = self.get_all_problems()
        for problem in problems['stat_status_pairs']:
            if problem['stat']['question_id'] == problem_id:
                return problem
        return None

import json
import os

class DataStorage:
    def __init__(self, filename='leetcode_problems.json', topics_filename='leetcode_topics.json'):
        self.filename = filename
        self.topics_filename = topics_filename
        self.initial_topics = ["Array", "String", "Hash Table", "Dynamic Programming", "Math",
                           "Sorting", "Greedy", "Depth-First Search", "Binary Search",
                           "Tree", "Graph", "Breadth-First Search", "Backtracking"]

    def has_problems_saved(self):
        """Check if problems are already saved"""
        return os.path.exists(self.filename) and os.path.getsize(self.filename) > 0

    def save_problems(self, problems):
        """Saves problems to a JSON file."""
        problems['stat_status_pairs'].reverse()
        with open(self.filename, 'w') as file:
            json.dump(problems, file, indent=4)

    def load_problems(self):
        """Loads problems from the JSON file."""
        if not self.has_problems_saved():
            return None
        with open(self.filename, 'r') as file:
            return json.load(file)

    def get_specific_problem(self, problem_id, display=False):
        """Gets a specific problem by ID."""
        problems = self.load_problems()
        for problem in problems['stat_status_pairs']:
            if problem['stat']['question_id'] == problem_id:
                # Modify the problem data for a clean output and add custom fields as needed
                if display:
                    return self.format_problem_output(problem)
                return problem
        return None

    def format_problem_output(self, problem):
        """Formats the problem for clean output."""
        formatted_problem = {
            'ID': problem['stat']['question_id'],
            'Title': problem['stat']['question__title'],
            'Difficulty': ['Easy', 'Medium', 'Hard'][problem['difficulty']['level'] - 1],
            # Add custom fields and additional formatting as needed
        }
        return formatted_problem

    def update_problem(self, problem_id: int, updated_data):
        problems = self.load_problems()
        for i, problem in enumerate(problems['stat_status_pairs']):
            if problem['stat']['question_id'] == problem_id:
                problems['stat_status_pairs'][i] = updated_data
                self.save_problems(problems)
                break


    def save_topics(self, topics):

        with open(self.topics_filename, 'w') as file:
            json.dump(topics, file)

    def load_topics(self):
        if not os.path.exists(self.topics_filename):
            formatted_topics = [{'name': topic, 'success': 0, 'failure': 0} for topic in self.initial_topics]
            self.save_topics(formatted_topics)
            return self.initial_topics
        with open(self.topics_filename, 'r') as file:
            return json.load(file)

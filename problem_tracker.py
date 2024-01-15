import random
from data_storage import DataStorage
import time
import threading

class ProblemTracker:
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self.predefined_topics = self.storage.load_topics()

    def start_solve_mode(self):
        choice = input("Enter '1' for a random problem, '2' for a specific problem: ")
        if choice == '1':
            self.solve_random_problem()
        elif choice == '2':
            problem_id = int(input("Enter problem ID: "))
            self.solve_specific_problem(problem_id)

    def solve_random_problem(self):
        problems = self.storage.load_problems()
        if not problems:
            print("No problems loaded. Please fetch problems first.")
            return

        random_problem = random.choice(problems['stat_status_pairs'])
        self.solve_problem(random_problem['stat']['question_id'])

    def solve_specific_problem(self, problem_id: int):
        problem = self.storage.get_specific_problem(problem_id)
        if problem:
            self.solve_problem(problem_id)
        else:
            print(f"No problem found with ID: {problem_id}")

    def solve_problem(self, problem_id: int):
        # Fetch problem details
        problem = self.storage.get_specific_problem(problem_id, True)
        print(f"Solving Problem: {problem['Title']} (ID: {problem_id})")

        # Start stopwatch
        start_time = time.time()
        input("Press Enter to stop the timer and return to the main menu.")
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        print(f"Time spent: {int(minutes)} minutes and {int(seconds)} seconds")

        # Log time and other details
        self.record_time_spent(problem_id, int(minutes))

    def record_solved_problem(self, problem_id: int):
        problem = self.storage.get_specific_problem(problem_id)
        if problem:
            # Solved or Failed (had to see solution)
            success = input("Successfully solved the problem (y/n)") == 'y'

            # Add or update fields
            problem['times_solved'] = problem.get('times_solved', 0) + 1
            # problem['solve_time'] = input("Enter solve time in minutes (optional): ") or None

            # Allow user to select topics or add a new one
            # Display existing topics
            for i, topic in enumerate(self.predefined_topics, 1):
                print(f"{i}. {topic['name']}")
            print(f"{len(self.predefined_topics) + 1}. Add a new topic")

            selected_topics_indices = input("Enter choices: ")
            selected_indices = selected_topics_indices.split(',')

            selected_topics = []
            for index in selected_indices:
                if int(index) == len(self.predefined_topics) + 1:
                    new_topic = input("Enter the new topic: ")
                    self.predefined_topics.append({'name': new_topic, 'success': 0, 'failure': 0})
                    selected_topics.append(new_topic)
                else:
                    selected_topics.append(self.predefined_topics[int(index) - 1])

                if success:
                    self.predefined_topics[int(index) - 1]['success'] += 1
                else:
                    self.predefined_topics[int(index) - 1]['failure'] += 1

            problem['topics'] = selected_topics
            self.storage.save_topics(self.predefined_topics)  # Save the updated topic list

            problem['comments'] = input("Any comments on the problem: ") or problem.get('comments', '')
            self.storage.update_problem(problem_id, problem)
            print(f"Problem {problem_id} updated.")
        else:
            print(f"No problem found with ID: {problem_id}")


    def start_timer(self, minutes: int):
        def timer():
            try:
                for _ in range(minutes * 60):
                    time.sleep(1)
                    # Update terminal with remaining time
            except KeyboardInterrupt:
                print("\nTimer cancelled.")

        timer_thread = threading.Thread(target=timer)
        timer_thread.start()
        print("Timer started. Press Ctrl+C to cancel.")

    def record_time_spent(self, problem_id: int, minutes: int):
        # Update problem with time spent
        problem = self.storage.get_specific_problem(problem_id)
        problem['solve_time'] = minutes
        # self.storage.update_problem(problem_id, problem)
        print(f"Updated problem {problem_id} with time spent: {minutes} minutes")
        self.record_solved_problem(problem_id)

from api_client import LeetCodeAPIClient
from data_storage import DataStorage
from problem_tracker import ProblemTracker
from analytics import *

# import tkinter as tk
# from tkinter import simpledialog
#
# def view_problem():
#     problem_id = simpledialog.askinteger("View Problem", "Enter Problem ID:")
#     problem = storage.get_specific_problem(problem_id)
#     if problem:
#         label.config(text=f"Problem: {problem}")
#     else:
#         label.config(text="Problem not found.")
#
# def start_solve_mode():
#     tracker.start_solve_mode()
#     # Update UI as needed after solve mode
#
# def record_solved_problem():
#     problem_id = simpledialog.askinteger("Record Problem", "Enter Problem ID to record as solved:")
#     tracker.record_solved_problem(problem_id)
#     # Update UI as needed
#
# def show_analytics():
#     # Implement functionality to show analytics
#     pass

# # Set up the main window
# root = tk.Tk()
# root.title("LeetCode Problem Tracker")
#
# storage = DataStorage()
# tracker = ProblemTracker(storage)
#
# # Create buttons and label
# view_button = tk.Button(root, text="View Specific Problem", command=view_problem)
# solve_button = tk.Button(root, text="Start Solve Mode", command=start_solve_mode)
# record_button = tk.Button(root, text="Record Solved Problem", command=record_solved_problem)
# analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics)
# label = tk.Label(root, text="Welcome to LeetCode Problem Tracker")
#
# # Layout
# view_button.pack()
# solve_button.pack()
# record_button.pack()
# analytics_button.pack()
# label.pack()
#
# # Start the GUI event loop
# root.mainloop()

def main():
    storage = DataStorage()
    tracker = ProblemTracker(storage)

    # Check if problems are already fetched and saved
    if not storage.has_problems_saved():
        print("Fetching and saving all problems...")
        client = LeetCodeAPIClient()
        problems = client.get_all_problems()
        storage.save_problems(problems)
        print("Problems fetched and saved.")
    else:
        print("Problems already fetched.")

    while True:
        choice = input("\nChoose an option:\n1. View Specific Problem\n2. Start Solve Mode\n3. Record Solved Problem\n4. Show Analytics\n5. Exit\n> ")

        if choice == '1':
            problem_id = int(input("Enter the problem ID: "))
            problem = storage.get_specific_problem(problem_id, True)
            if problem:
                print("Problem details:", problem)
            else:
                print(f"No problem found with ID {problem_id}.")
        elif choice == '2':
            tracker.start_solve_mode()
        elif choice == '3':
            problem_id = int(input("Enter problem ID to record as solved: "))
            tracker.record_solved_problem(problem_id)
        elif choice == '4':
            # Show analytics
            data = storage.load_problems()
            if data:
                plot_topic_strength(data)
            else:
                print("No data available for analytics.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

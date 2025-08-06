# Import necessary modules from Python standard library
import json
import os
from datetime import datetime, timedelta


# Represents a single task in the scheduler
class Task:
    def __init__(self, title, description, priority, due_date, completed=False):
        self.title = title 
        self.description = description  
        self.priority = priority 
        self.due_date = due_date  
        self.completed = completed 


    # Convert Task object to dictionary for JSON serialization
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed
        }


    # Create a Task object from a dictionary (used when loading from JSON)
    @staticmethod
    def from_dict(data):
        return Task(
            data["title"],
            data["description"],
            data["priority"],
            data["due_date"],
            data.get("completed", False)
        )


# Manages the list of tasks and handles all operations and persistence
class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename 
        self.tasks = []  
        self.load_tasks()  


    # Add a new task to the list
    def add_task(self, title, description, priority, due_date):
        task = Task(title, description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks() 


    # Display all tasks in a readable format
    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        print("\nAll Tasks:")
        for idx, task in enumerate(self.tasks, 1):
            status = "Complete" if task.completed else "Incomplete"
            print(f"[{idx}] {task.title} | Due: {task.due_date} | Priority: {task.priority} | Status: {status}")
            print(f"    Description: {task.description}")


    # Sort and display tasks by due date or priority
    def sort_tasks(self, by="due_date"):
        if by == "due_date":
            sorted_tasks = sorted(self.tasks, key=lambda t: t.due_date)
        elif by == "priority":
            sorted_tasks = sorted(self.tasks, key=lambda t: t.priority)
        else:
            sorted_tasks = self.tasks
        if not sorted_tasks:
            print("No tasks to sort.")
            return
        print(f"\nTasks sorted by {by.replace('_', ' ').title()}:")
        for idx, task in enumerate(sorted_tasks, 1):
            status = "Complete" if task.completed else "Incomplete"
            print(f"[{idx}] {task.title} | Due: {task.due_date} | Priority: {task.priority} | Status: {status}")


    # Mark a task as complete by its index
    def mark_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()
            print(f"Task '{self.tasks[index].title}' marked as complete.")
        else:
            print("Invalid task number.")


    # Show summary: total, incomplete, and tasks due soon
    def view_summary(self):
        total = len(self.tasks)
        incomplete = sum(not t.completed for t in self.tasks)
        today = datetime.today()
        soon = []
        for t in self.tasks:
            try:
                due = datetime.strptime(t.due_date, "%Y-%m-%d")
                # Check if task is incomplete and due within next 3 days
                if not t.completed and 0 <= (due - today).days <= 3:
                    soon.append(t)
            except Exception:
                continue
        print("\nSummary:")
        print(f"Total tasks: {total}")
        print(f"Incomplete tasks: {incomplete}")
        print(f"Tasks due in next 3 days: {len(soon)}")
        for t in soon:
            print(f"    {t.title} (Due: {t.due_date})")


    # Save all tasks to JSON file
    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)


    # Load tasks from JSON file if it exists
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(d) for d in data]
            except Exception:
                self.tasks = []
        else:
            self.tasks = []


# Prompt user for a valid date in YYYY-MM-DD format
def input_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


# Prompt user for a valid priority (integer 1-5)
def input_priority(prompt):
    while True:
        val = input(prompt)
        if val.isdigit() and 1 <= int(val) <= 5:
            return int(val)
        print("Priority must be an integer between 1 and 5.")


# Print the main menu options
def main_menu():
    print("\n==== Task Scheduler ====")
    print("1. Add a Task")
    print("2. List All Tasks")
    print("3. Sort Tasks by Due Date")
    print("4. Sort Tasks by Priority")
    print("5. Mark Task as Complete")
    print("6. View Summary")
    print("7. Exit")


# Main loop for the CLI application
def main():
    manager = TaskManager() 
    while True:
        main_menu()  # Show menu
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            # Add a new task
            title = input("Enter task title: ").strip()
            description = input("Enter description: ").strip()
            priority = input_priority("Enter priority (1-5): ")
            due_date = input_date("Enter due date (YYYY-MM-DD): ")
            manager.add_task(title, description, priority, due_date)
            print("Task added successfully.")
        elif choice == "2":
            # List all tasks
            manager.list_tasks()
        elif choice == "3":
            # Sort tasks by due date
            manager.sort_tasks(by="due_date")
        elif choice == "4":
            # Sort tasks by priority
            manager.sort_tasks(by="priority")
        elif choice == "5":
            # Mark a task as complete
            manager.list_tasks()
            if manager.tasks:
                try:
                    idx = int(input("Enter task number to mark as complete: ")) - 1
                    manager.mark_complete(idx)
                except ValueError:
                    print("Invalid input.")
        elif choice == "6":
            # View summary
            manager.view_summary()
        elif choice == "7":
            # Exit the program
            print("Exiting Task Scheduler. Goodbye!")
            break
        else:
            print("Invalid option. Please select 1-7.")


if __name__ == "__main__":
    main()

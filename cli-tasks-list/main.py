import time
from progressbar import ProgressBar

class TaskManager:
    def __init__(self):
        self.tasks = []

    def view_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            print("\nTasks:")
            for index, task in enumerate(self.tasks, start=1):
                status = "Completed" if task["completed"] else "Pending"
                print(f"{index}. {task['title']} - {status}")

    def add_task(self):
        title = input("Enter task title: ")
        self.tasks.append({"title": title, "completed": False})
        print("Task added.")

    def edit_task(self):
        self.view_tasks()
        task_index = int(input("Enter the task number to edit: ")) - 1
        if 0 <= task_index < len(self.tasks):
            new_title = input("Enter new task title: ")
            self.tasks[task_index]["title"] = new_title
            print("Task updated.")
        else:
            print("Invalid task number.")

    def delete_task(self):
        self.view_tasks()
        task_index = int(input("Enter the task number to delete: ")) - 1
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)
            print("Task deleted.")
        else:
            print("Invalid task number.")

    def select_task(self):
        self.view_tasks()
        task_index = int(input("Enter the task number you worked on: ")) - 1
        if 0 <= task_index < len(self.tasks):
            return self.tasks[task_index]["title"]
        else:
            print("Invalid task number.")
            return None

    def mark_completed(self, task_title):
        for task in self.tasks:
            if task["title"] == task_title:
                task["completed"] = True
                break

    def generate_report(self):
        completed_tasks = [task for task in self.tasks if task["completed"]]
        pending_tasks = [task for task in self.tasks if not task["completed"]]

        print("\nReport:")
        print("Completed Tasks:")
        for task in completed_tasks:
            print(f"- {task['title']}")

        print("\nPending Tasks:")
        for task in pending_tasks:
            print(f"- {task['title']}")

class PomodoroTimer:
    def __init__(self, work_interval, break_interval, cycles):
        self.work_interval = work_interval * 60  # Convert to seconds
        self.break_interval = break_interval * 60  # Convert to seconds
        self.cycles = cycles

    def start(self):
        for cycle in range(1, self.cycles + 1):
            print(f"\n--- Pomodoro Cycle {cycle} ---")
            self._run_session("Work", self.work_interval)
            self._run_session("Break", self.break_interval)

    def _run_session(self, session_type, duration):
        print(f"{session_type} session started!")
        progress = ProgressBar(maxval=duration).start()
        for i in range(duration):
            time.sleep(1)
            progress.update(i + 1)
        progress.finish()
        print(f"{session_type} session completed!")

def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def print_menu():
    print("\nFocus Flow - Pomodoro Technique Task Manager")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Start Pomodoro Timer")
    print("6. View Reports")
    print("7. Exit")

def main():
    todo_list = TaskManager()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            todo_list.view_tasks()
        elif choice == "2":
            todo_list.add_task()
        elif choice == "3":
            todo_list.edit_task()
        elif choice == "4":
            todo_list.delete_task()
        elif choice == "5":
            work_interval = get_integer_input("Enter work interval (minutes): ")
            break_interval = get_integer_input("Enter break interval (minutes): ")
            cycles = get_integer_input("Enter number of Pomodoro cycles: ")

            pomodoro_timer = PomodoroTimer(work_interval, break_interval, cycles)
            pomodoro_timer.start()

            completed_task = todo_list.select_task()
            if completed_task:
                todo_list.mark_completed(completed_task)
                print(f"Task '{completed_task}' marked as completed.")
        elif choice == "6":
            todo_list.generate_report()
        elif choice == "7":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

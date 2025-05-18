"""Create a class called "Task" that takes when initialized has a title, priority, and a due_date attributes"""

from datetime import datetime, timedelta

import csv


class Task:

    tasks = []

    def __init__(self, title="task_title", days_to_complete=0, date_created=None, date_due=None):

        self.title = title

        self.days_to_complete = days_to_complete

        # creates instance variable for the current date task was created.
        if date_created:
            try:
                self.date_created = datetime.strptime(date_created, "%Y-%m-%d").date()
            except ValueError:
                print(
                    "Pre-exisiting 'Date Created' in incorrect format. Expected: YYYY-MM-DD."
                )
                # fallback set date_created to current date
                self.date_created = datetime.today().date()
        else:
            self.date_created = datetime.today().date()

        # creates a "task.due_date" instance variable by summing the date the task was created
        # and a time delta conversion for the int number of days to complete the task.
        if date_due:
            try:
                self.date_due = datetime.strptime(date_due, "%Y-%m-%d").date()
            except ValueError:
                print(
                    "Pre-exisiting 'Date Created' in incorrect format. Expected: YYYY-MM-DD."
                )
                # fallback set date_created to current date
                self.date_due = datetime.today().date()
        else:
            self.date_due = Task.set_date_due(self, days_to_complete)

        self.priority = Task.set_priority(self, days_to_complete)

        Task.tasks.append(self)

    @classmethod
    def load_tasks_file(cls):
        try:
            with open("tasks.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                next(reader, None)  # skip over the header row

                rows_found = False  # flag for detecting if rows in reader after header
                for row in reader:
                    rows_found = True  # switch flag to true, rows found
                    try:
                        task_title = row[0]
                        date_created = row[2]
                        date_due = row[3] 
                        days_to_complete = int(row[4])
                        cls(task_title, days_to_complete, date_created, date_due)
                    except ValueError:
                        print("Invalid data encountered in row, skipping row.")
                if not rows_found:
                    pass

        except FileNotFoundError:
            print("Previous task list not found. Creating new task list.")
            with open("tasks.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "title",
                        "priority",
                        "date_created",
                        "date_due",
                        "days_to_complete",
                    ]
                )
            print("New task list file created.")

    @classmethod
    def save_task_file(cls):
        with open("tasks.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["title", "priority", "date_created", "date_due", "days_to_complete"]
            )
            for task in cls.tasks:
                writer.writerow(
                    [
                        task.title,  # index 0
                        task.priority,  # index 1
                        task.date_created,  # index 2
                        task.date_due,  # index 3
                        task.days_to_complete,  # index 4
                    ]
                )

    @classmethod
    def existing_task(cls, title):
        for task in cls.tasks:
            if task.title == title:
                return task
        return None

    @classmethod
    def sort_tasks(cls):
        cls.tasks = sorted(cls.tasks, key=lambda task: task.days_to_complete)

    @classmethod
    def filter_tasks(cls, priority_filter: int):
        index = 0
        priority_found = False
        for task in cls.tasks:
            if task.priority == priority_filter:
                index += 1
                priority_found = True
                print(f"\t{index}. {task.title}")

        if priority_found == False:
            print(f"No Priority {priority_filter} Tasks")

    @classmethod
    def display_tasks(cls, key=""):
        if (
            cls.tasks
        ):  # if there are values/object (tasks) in the tasks list do the following:
            print(f"\nCurrent Tasks:\n")

            if key == "":
                index = 0
                for task in cls.tasks:
                    index += 1
                    print(f"\t{index}. {task.title} | Due: {task.date_due}")

            elif key == "priority_1":
                Task.filter_tasks(1)

            elif key == "priority_2":
                Task.filter_tasks(2)

            elif key == "priority_3":
                Task.filter_tasks(3)
        else:
            print(f"\nNo tasks in Task List, please add a task.")
            return None

    @classmethod
    def remove_task(cls, task):
        cls.tasks.remove(task)

    @classmethod
    def clear_tasks_list(cls):
        cls.tasks.clear()

    def set_priority(self, days_to_complete):
        if days_to_complete in range(0, 4):
            self.priority = 1
        elif days_to_complete in range(4, 8):
            self.priority = 2
        elif days_to_complete > 7:
            self.priority = 3
        else:
            self.priority = 0  # 0 priority, task is expired
        return self.priority

    def set_date_due(self, days_to_complete):
        self.date_due = self.date_created + timedelta(days=days_to_complete)
        return self.date_due

    def update_task(self, new_days_to_complete):
        self.days_to_complete = new_days_to_complete
        self.set_date_due(new_days_to_complete)
        self.set_priority(new_days_to_complete)

    def __repr__(self):
        return f"Task(title={self.title}, priority={self.priority}, date_created={self.date_created}, date_due={self.date_due})"


# job1 = Task(title="Do the dishes", days_to_complete=5)
# job1 = Task(title="clean", days_to_complete=1)
# job1 = Task(title="cook", days_to_complete=4)
# job1 = Task(title="code", days_to_complete=9)

# job1.display_tasks()

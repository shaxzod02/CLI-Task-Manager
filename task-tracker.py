import sys
from task_class import Task
from globals import *
import cowsay
import os
from cowsay_animals import cowsay_animals
import datetime

user_animal = "cow"
expired_tasks = []


def main():
    """Main funtion call to launch the system or close"""
    while True:
        clear_terminal()
        user_input = input(f"Would you like to open {SYS_NAME}?\n[1]: Yes\n[2]: No\n")

        if user_input == "1":
            Task.load_tasks_file()  # load the pre-existing tasks
            update_days_to_complete()  # update the days to complete according to current date prog run

            for (
                task
            ) in (
                Task.tasks
            ):  # update the priority according to the new days to complete
                Task.set_priority(task, days_to_complete=task.days_to_complete)

            check_expired_tasks()  # check if any tasks are expired
            display_expired_tasks()  # display the expired tasks to the user
            run_sys()  # run system
        elif user_input == "2":
            sys.exit()
        else:
            print("Invalid Input")
            continue


def run_sys():
    """"""
    while True:
        clear_terminal()
        cowsay_message(message=INTRODUCTION)
        # cowsay.cow(INTRODUCTION)
        user_input = input(
            f"\nPlease select from the following options:"
            f"\n[1]: Add New Task"
            f"\n[2]: Edit Task List"
            f"\n[3]: View Task List"
            f"\n[4]: Exit\n"
        )
        if user_input == "1":
            add_task()
            Task.sort_tasks()
            continue
        elif user_input == "2":
            edit_task_list()
            continue
        elif user_input == "3":
            Task.sort_tasks()
            display_tasks()
        elif user_input == "4":
            Task.save_task_file()
            sys.exit()
        elif user_input == "animal":
            # speical feature! change the cowsay animal display
            change_animal()

        else:
            print("Invalid Input")
            continue


def add_task():
    clear_terminal()
    while True:
        cowsay_message(message="Let's add a new task!")
        task_title = input("Title Task: ").title().strip()
        # using the @classmethod existing_task() check to see if there is already a task w/ the same title.
        existing_task = Task.existing_task(task_title)
        if existing_task:
            clear_terminal()
            print(f"\nTask already created, please try a diffent title.\n")
            continue
        break
    while True:
        try:
            task_days_to_complete = int(input(f"How Many Days to Complete: "))
            break
        except ValueError:
            print("Please enter a number.")
            continue

    Task(
        title=task_title,
        days_to_complete=(task_days_to_complete),
    )
    clear_terminal()


def edit_task_list():
    clear_terminal()
    if Task.tasks:
        while True:
            cowsay_message(message="Let's Edit the Task List!")
            user_input = input(
                f"\nHow would you like to edit the task list?\n"
                f"\nPlease select from the following options:"
                f"\n[1]: Edit Task Property"
                f"\n[2]: Remove Task"
                f"\n[3]: Clear Task List"
                f"\n[4]: Main Menu\n"
            )
            if user_input == "1":
                edit_task_property()
                break
            elif user_input == "2":
                remove_task()
                break
            elif user_input == "3":
                clear_tasks()
                break
            elif user_input == "4":
                break
            else:
                clear_terminal()
                print(f"Invalid Input '{user_input}', please enter a valid number.")
                continue
        run_sys()
    else:
        cowsay_message(message="No Tasks To Edit!")
        user_input = input("\nPress any key to exit.")
        if user_input or user_input == "":
            clear_terminal()
            run_sys


def edit_task_property():
    clear_terminal()
    cowsay_message(message="Here Are Your Current Tasks!")
    Task.display_tasks()
    while True:
        try:
            task_to_edit_numbered = int(input("\nWhich task would you like to edit?: "))
            task_to_edit_index = task_to_edit_numbered - 1
            if task_to_edit_index < 0 or task_to_edit_index >= len(Task.tasks):
                print(
                    f"Invalid Input '{task_to_edit_numbered}'. Enter a number associated with a task."
                )
                continue
            break
        except ValueError:
            clear_terminal()
            print("Please enter the task rank/number.")
            continue

    task_to_edit = Task.tasks[task_to_edit_index]

    while True:
        clear_terminal()
        cowsay_message(message="Select Parameter to Edit!")
        user_input = input(
            f"\nPlease select a Task parameter to edit:"
            f"\n[1]: Task Title"
            f"\n[2]: Days To Complete"
            f"\n[3]: Main Menu\n"
        )
        if user_input == "1":
            clear_terminal()
            cowsay_message(message="Update Task Title!")
            new_title = input("New Task Title: ").title().strip()
            task_to_edit.title = new_title
            continue
        elif user_input == "2":
            while True:
                clear_terminal()
                cowsay_message(message="Update Task's Days to Complete!")
                try:
                    days_to_complete_edit = int(input("New Days to Complete Task: "))
                    Task.update_task(task_to_edit, days_to_complete_edit)
                    break
                except ValueError:
                    clear_terminal()
                    print(f"Invalid Input, Please Enter a Number")
                    continue

        elif user_input == "3":
            Task.sort_tasks()
            clear_terminal()
            run_sys()
        else:
            clear_terminal()
            print("Invalid Input")
            continue


def remove_task():

    while True:
        clear_terminal()
        cowsay_message(message="Remove a Task!")
        Task.display_tasks()
        try:
            task_to_remove_numbered = int(
                input("\nWhich task would you like to remove?: ")
            )
            task_to_remove_index = task_to_remove_numbered - 1
            break
        except ValueError:
            print("Please enter the task rank/number.")
            continue

    task_to_remove = Task.tasks[task_to_remove_index]

    Task.remove_task(task_to_remove)


def clear_tasks():
    while True:
        clear_terminal()
        cowsay_message(message="Clear Task List")
        user_input = input(
            f"\nAre you sure?\n" "\n[1]: Yes, Clear Task List" "\n[2]: Go Back\n"
        )
        if user_input == "1":
            Task.clear_tasks_list()
            run_sys()
        elif user_input == "2":
            edit_task_list()
        else:
            print("Invalid Input")
            continue


def display_tasks():
    while True:
        clear_terminal()
        cowsay_message(message="Here Are Your Current Tasks!")
        Task.display_tasks()

        user_input = input(
            "\nPlease select from the following options:"
            "\n[1]: Filter Tasks"
            "\n[2]: Main Menu\n"
        )
        if user_input == "1":
            filter_tasks()
        elif user_input == "2":
            run_sys()
        else:
            print("Invalid Input")
            continue


def filter_tasks():
    while True:
        clear_terminal()

        cowsay_message(message="Select a Filter Parameter!")
        user_input = input(
            "\nFilter Parameters:"
            "\n[1]: View Priority 1 Tasks"
            "\n[2]: View Priority 2 Tasks"
            "\n[3]: View Priority 3 Tasks"
            "\n[4]: Main Menu\n"
        )
        if user_input == "1":
            clear_terminal()
            cowsay_message(message="Prioirty 1 Tasks!")
            Task.display_tasks(key="priority_1")
            while True:
                user_input = input("\nPress 'q' to quit Expired Tasks view.\n")
                if user_input == "q":
                    break
                else:
                    continue
        elif user_input == "2":
            clear_terminal()
            cowsay_message(message="Prioirty 2 Tasks!")
            Task.display_tasks(key="priority_2")
            while True:
                user_input = input("\nPress 'q' to quit Expired Tasks view.\n")
                if user_input == "q":
                    break
                else:
                    continue
        elif user_input == "3":
            clear_terminal()
            cowsay_message(message="Prioirty 3 Tasks!")
            Task.display_tasks(key="priority_3")
            while True:
                user_input = input("\nPress 'q' to quit Expired Tasks view.\n")
                if user_input == "q":
                    break
                else:
                    continue
        elif user_input == "4":
            run_sys()
        else:
            print("Invalid Input")
            continue


def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def change_animal():
    clear_terminal()
    cowsay_animals
    global user_animal
    while True:
        cowsay_message(message="why don't you want me?")

        for index, animal in enumerate(cowsay_animals):
            print(f"{index+1}. {animal}")
        try:
            user_input = int(input("Please Select an Animal: "))
            if 1 <= user_input <= len(cowsay_animals):
                user_animal_index = user_input - 1
                user_animal = cowsay_animals[user_animal_index]
                clear_terminal()
                return user_animal
            else:
                clear_terminal()
                print("Invalid Input.\nPlease enter a valid number.")
        except ValueError:
            clear_terminal()
            print("Invalid Input.\nPlease enter a number.")
            continue


def update_days_to_complete():
    """Logs the current date. Edits the days to complete attribute for each
    task according to the current date."""
    date_current = datetime.date.today()
    for task in Task.tasks:
        task.days_to_complete = task.date_due - date_current
        # convert timedelta object "days" back into int value
        task.days_to_complete = task.days_to_complete.days


def check_expired_tasks():
    """Checks tasks days to complete, if negative (expired/overdue) the task is
    removed from the list and appended to an expired list."""
    for task in Task.tasks[:]:
        if task.days_to_complete < 0:
            Task.tasks.remove(task)
            global expired_tasks
            expired_tasks.append(task)


def display_expired_tasks():
    clear_terminal()
    global expired_tasks
    cowsay_message(message="These task(s) expired while you were away.")
    if expired_tasks:
        print("\nExpired Tasks:\n")  # header
        for index, task in enumerate(expired_tasks):
            print(f"{index+1}. {task.title} | Expired: {task.date_due}")
    else:
        print("No expired tasks")
    while True:
        user_input = input("\nPress 'q' to quit Expired Tasks view.\n")

        if user_input == "q":
            break
        else:
            continue


def cowsay_message(animal=None, message="moo"):
    animal = animal or user_animal
    animal_message = getattr(cowsay, animal)

    animal_message(message)


main()

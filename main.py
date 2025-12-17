import json


def decorated_list(input_func):
    def output_func(self):
        print('-' * 20)
        input_func(self)
        print('-' * 20)

    return output_func


class Task:
    def __init__(self, task_id, title, description, status=False):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status


class ToDoList:
    def __init__(self, file_name):
        self.tasks = []
        self.load_from_json(file_name)
        self.completed_tasks = []


    def save_to_json(self, file_name):
        data_to_save = [t.__dict__ for t in self.tasks]
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, ensure_ascii=False)

    def load_from_json(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
                for item in tasks:
                    self.tasks.append(Task(item['id'], item['title'], item['description'], item['status']))
        except (FileNotFoundError, json.JSONDecodeError):
            print("File not found.. create new one list")
            self.tasks = []

    def id_reload(self):
        for index, t in enumerate(self.tasks, start=1):
            t.id = index


    def status_check(self):
        completed = [t for t in self.tasks if t.status]

        if not completed:
            print("No matches")
            return

        for t in completed:
            self.completed_tasks.append(t)
            self.tasks.remove(t)


    def mark_task(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                t.status = True
                print("Marked completed")
                self.status_check()
                break
        else:
            print("No matches")


    def add_task(self, title, description):
        new_id = len(self.tasks) + 1
        new_task = Task(new_id, title, description)
        self.tasks.append(new_task)


    def del_task(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                self.tasks.remove(t)
                print("Removed task:", t.title)
                self.id_reload()
                break
        else:
            print("No matches")


    @decorated_list
    def show_tasks(self):
        if not self.tasks:
            print("Empty list")
        for t in self.tasks:
            status = "✅" if t.status else "❌"
            print(f"{t.id}. {t.title} [{status}]")

    @decorated_list
    def show_completed_tasks(self):
        print("Here your completed task list:")
        if not self.completed_tasks:
            print("Empty list")
        for t in self.completed_tasks:
            status = "✅" if t.status else "❌"
            print(f"{t.id}. {t.title} [{status}]")


f_name = "data.json"
my_list = ToDoList(f_name)

try:
    while True:
        print()
        print("Here your current Tasks: ")
        my_list.show_tasks()

        print("1 - mark task completed\n2 - add new task\n3 - delete task\n4 - view completed tasks\n5 - exit")
        which_option = int(input("Write what do you want to do: "))
        match which_option:
            case 1:
                task_id = int(input("Enter a task's id: "))
                my_list.mark_task(task_id)

            case 2:
                while True:
                    task_title = input("Enter the title: ")
                    if len(task_title) <= 1:
                        print("Write at least 2 symbols")
                        continue

                    task_description = input("Enter the description: ")
                    my_list.add_task(task_title, task_description)
                    print("Successfully added")
                    break
            case 3:
                task_id = int(input("Enter a task's id: "))
                my_list.del_task(task_id)

            case 4:
                my_list.show_completed_tasks()
            case 5:
                print("Shutting down program..")
                break
except KeyboardInterrupt:
    print("Detected some suddenly shutdown..\nSaving tasks..")
finally:
    print("Tasks saved")
    my_list.save_to_json(f_name)
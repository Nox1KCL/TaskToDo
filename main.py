import json
import os
from typing import List, Dict, Any, Optional


# region Functions
def overviewTasks(tasks: list[dict[str, Any]], prettyTasksList: str) -> None:
    consoleCleaner()
    if isEmpty(tasks):
        waitForEnter()
        saveTasks(tasks)
        return

    print("Here you are!\n", prettyTasksList, "\n")
    waitForEnter()


def createNewTask(tasks: list[dict[str, Any]]) -> None:
    taskName = input("Enter Name of Task: ")
    currentId = getNextId(tasks)

    newTask = {"id": currentId, "Name": taskName, "done": False}

    tasks.append(newTask)
    prettyNewTask = json.dumps(newTask, indent=2, ensure_ascii=False)
    consoleCleaner()
    print("Here you are!\n", prettyNewTask)
    waitForEnter()


def deleteTask(tasks: list[dict[str, Any]], prettyTasksList: str) -> None:
    isEmpty(tasks)
    consoleCleaner()
    overviewTasks(tasks, prettyTasksList)

    taskIndex = indexAndNoneChecking(tasks)
    if taskIndex is None:
        print("Index error")
        waitForEnter()
        saveTasks(tasks)
        return

    deletedTask = tasks.pop(taskIndex)
    print(f"Deleted Task: Id {deletedTask['id']} - '{deletedTask['Name']}'")
    waitForEnter()


def manageTask(tasks: list[dict[str, Any]], prettyTasksList: str) -> None:
    isEmpty(tasks)
    consoleCleaner()
    overviewTasks(tasks, prettyTasksList)

    taskIndex = indexAndNoneChecking(tasks)
    if taskIndex is None:
        print("Index error")
        waitForEnter()
        saveTasks(tasks)
        return

    taskToManage = tasks[taskIndex]

    newTaskName = input("Enter new task name(Enter to skip): ").strip()
    if newTaskName == "":
        newTaskName = taskToManage["Name"]

    taskToManage["Name"] = newTaskName
    isDone = input('Press Enter to mark "Completed"(0 to Uncompleted): ')
    if isDone == "":
        taskToManage["done"] = True

    prettyUpdatedTask = json.dumps(taskToManage, indent=2, ensure_ascii=False)

    consoleCleaner()
    print("UpdatedTask: ", prettyUpdatedTask)
    waitForEnter()
    consoleCleaner()


def finishWork(tasks: List[Dict[str, Any]]) -> bool:
    print("Finishing work..")
    saveTasks(tasks)
    return False


def waitForEnter() -> None:
    while True:
        userInput = input("Press Enter to Resume..").strip()
        if not userInput:
            break
        else:
            print("Please, press ONLY Enter")


def getNextId(tasks: List[Dict[str, Any]]) -> int:
    if not tasks:
        return 1
    else:
        maxId = max(item["id"] for item in tasks)
        return maxId + 1


def consoleCleaner() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def isEmpty(tasks: List[Dict[str, Any]]) -> bool:
    if not tasks:
        print("All task completed!")
        return True
    return False


def findTaskById(tasks: List[Dict[str, Any]], chosenId: int) -> Optional[int]:
    for index, task in enumerate(tasks):
        if task["id"] == chosenId:
            foundTask = index
            return foundTask
    return None


def loadTasks() -> List[Dict[str, Any]]:
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            content = file.read()
            if not content:
                return []

            return json.loads(content)

    except json.JSONDecodeError:
        print("Помилка: Файл задач містить некоректний JSON-формат.")
        return []


def saveTasks(tasks: List[Dict[str, Any]]) -> None:
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Помилка при збереженні файлу: {e}")


def indexAndNoneChecking(tasks: List[Dict[str, Any]]) -> Optional[int]:
    try:
        chosenId = int(input("Enter task's id to manage it(0 to abort): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        waitForEnter()
        return None

    if chosenId == 0:
        waitForEnter()
        saveTasks(tasks)
        return None

    taskIndex = findTaskById(tasks, chosenId)
    if taskIndex is None:
        print("Incorrect index")
        waitForEnter()
        consoleCleaner()
        saveTasks(tasks)
        return None

    return taskIndex


# endregion

FILE_NAME = "tasks.json"
isWorking = True
tasks = loadTasks()
try:
    while isWorking:
        consoleCleaner()

        prettyTasksList = json.dumps(tasks, indent=2, ensure_ascii=False)

        isEmpty(tasks)

        choice = input(
            "Choose option:\n"
            "------------\n"
            "1 - Overview Tasks\n"
            "2 - Create New Task\n"
            "3 - Delete Task\n"
            "4 - Manage Task\n"
            "0 - Finish work\n"
            "------------\n"
            "Your answer: "
        )

        match choice:
            case "1":
                overviewTasks(tasks, prettyTasksList)
            case "2":
                createNewTask(tasks)
            case "3":
                deleteTask(tasks, prettyTasksList)
            case "4":
                manageTask(tasks, prettyTasksList)
            case "0":
                isWorking = finishWork(tasks)
            case _:
                print("Unknown command")
                waitForEnter()
                consoleCleaner()

except KeyboardInterrupt:
    print("\n\nThe program was interrupted by the user. (Ctrl+C)...")
    finishWork(tasks)
    print("Datas saved.")

"""
User should be able to create Task of type Story, Feature, Bugs.
Each can have their own status.
Stories can further have subtracts. SUB-TASK
Should be able to change the status of any task.
User should be able to create any sprint.
Should be able to add any task to sprint and remove from it.
User should be able to print Delayed task
Sprint details Tasks assigned to the user based on Task Status Will see all Task
get all disableTask of sprint
"""
import datetime
from enum import Enum


class TaskType(Enum):
    Story = "STORY"
    Feature = "FEATURE"
    Bugs = "BUGS"


class TaskStatus(Enum):
    Pending = "PENDING"
    Ongoing = "ONGOING"
    Completed = "COMPLETED"
    Disabled = "DISABLED"


class UnAuthorized(Exception):
    pass


class User:

    def __init__(self, name: str, position: str, team: str):
        self.name = name
        self.position = position
        self.team = team

    def create_sprint(self, name: str, start_date: datetime.datetime, end_date: datetime.datetime):
        if self.position == "PM":
            return Sprint(name, start_date, end_date)
        raise UnAuthorized

    def __str__(self):
        return f"{self.name}"


class Task:

    def __init__(self, type_: TaskType, name: str, description: str, user: User):
        self.name = name
        self.user = user
        self.description = description
        self.type = type_
        self.status = TaskStatus.Pending

    def set_status(self, status: TaskStatus):
        self.status = status

    def __str__(self):
        return f"Task: {self.name}: {self.user}"


class Sprint:

    def __init__(self, name: str, start_date: datetime.datetime, end_date: datetime.datetime):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = set()

    def add_task(self, task: Task):
        self.tasks.add(task)

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)

    def get_delayed_tasks(self):
        delayed_tasks = []
        for task in self.tasks:
            if task.status != TaskStatus.Completed:
                delayed_tasks.append(task)
        return delayed_tasks

    def get_disabled_tasks(self):
        disabled_tasks = []
        for task in self.tasks:
            if task.status == TaskStatus.Disabled:
                disabled_tasks.append(task)
        return disabled_tasks


def main():
    user1 = User("Jane", "PM", "Ops")
    start_date = datetime.datetime.utcnow()
    end_date = datetime.timedelta(14) + start_date
    sprint = user1.create_sprint("sprint1", start_date, end_date)
    dev1 = User("John", "SDE", "Engg")
    task = Task(TaskType.Feature, "add button", "Add a button to switch between the maps", dev1)
    sprint.add_task(task)
    print(sprint.get_delayed_tasks())


if __name__ == "__main__":
    main()

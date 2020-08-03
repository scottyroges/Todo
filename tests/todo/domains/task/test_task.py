import datetime

from freezegun import freeze_time

from app.todo.domains.action import Action
from app.todo.domains.category import Category
from app.todo.domains.tag import Tag
from app.todo.domains.task.task import Task
from app.todo.domains.todo_owner import TodoOwner


@freeze_time("2019-02-24 10:00:04")
def test_to_dict():
    todo_owner = TodoOwner(owner_id="123")
    tags = [Tag(name="who"), Tag(name="knows")]
    actions = [Action(action_id="fgh", points=2)]
    task = Task(todo_id="abc",
                todo_owner=todo_owner,
                name="task",
                description="description",
                completion_points=1,
                due_date=datetime.datetime(2019, 3, 2, 11, 32, 5),
                category=Category(category_id="abc",
                                  name="test",
                                  color="#FFF"),
                tags=tags,
                actions=actions)

    assert task.to_dict() == {
        "todoId": "abc",
        "todoOwnerId": "123",
        "name": "task",
        "description": "description",
        "todoType": "TASK",
        "completionPoints": 1,
        "dueDate": datetime.datetime(2019, 3, 2, 11, 32, 5),
        "category": {
            "id": "abc",
            "name": "test",
            "color": "#FFF"
        },
        "tags": ["who", "knows"],
        "createdDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
        "modifiedDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
        "actions": [{
            "actionId": "fgh",
            "actionDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
            "points": 2
        }],
        "shouldShow": False
    }


def test_should_show_no_action():
    todo_owner = TodoOwner(owner_id="123")
    task = Task(todo_id="abc",
                todo_owner=todo_owner,
                name="task",
                description="description",
                completion_points=1,
                due_date=datetime.datetime(2019, 3, 2, 11, 32, 5))

    assert task.should_show is True


def test_should_show_action():
    todo_owner = TodoOwner(owner_id="123")
    actions = [Action(action_date=datetime.datetime(2019, 3, 2, 10, 0, 0),
                      points=2)]
    task = Task(todo_id="abc",
                todo_owner=todo_owner,
                name="task",
                description="description",
                completion_points=1,
                due_date=datetime.datetime(2019, 3, 2, 11, 32, 5),
                actions=actions)

    assert task.should_show is False

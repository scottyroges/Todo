import datetime

from freezegun import freeze_time

from app.todo.domains.action import Action
from app.todo.domains.category import Category
from app.todo.domains.tag import Tag
from app.todo.domains.todo import Todo
from app.todo.domains.todo_owner import TodoOwner
from app.todo.domains.todo_type import TodoType


@freeze_time("2019-02-24 10:00:04")
def test_to_dict():
    todo_owner = TodoOwner(owner_id="123")
    tags = [Tag(name="who"), Tag(name="knows")]
    actions = [Action(action_id="fgh", points=2)]
    todo = Todo(todo_id="abc",
                todo_owner=todo_owner,
                name="todo",
                description="description",
                todo_type=TodoType.TASK,
                completion_points=1,
                category=Category(category_id="abc",
                                  name="test",
                                  color="#FFF"),
                tags=tags,
                actions=actions)

    assert todo.to_dict() == {
        "todoId": "abc",
        "todoOwnerId": "123",
        "name": "todo",
        "description": "description",
        "todoType": "TASK",
        "completionPoints": 1,
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
        "shouldShow": True
    }


def test_last_action_none():
    todo = Todo()

    assert todo.last_action is None


def test_last_action_none():
    todo = Todo()
    todo.perform_action(Action(action_date=datetime.datetime(2019, 3, 6)))
    todo.perform_action(Action(action_date=datetime.datetime(2019, 3, 4)))
    todo.perform_action(Action(action_date=datetime.datetime(2019, 3, 1)))

    assert todo.last_action is not None
    assert todo.last_action.action_date == datetime.datetime(2019, 3, 6)

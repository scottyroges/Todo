import datetime
import uuid

from app.model import Category, Habit, Tag, Action, Reoccur, Task
from app.todo.domains.todo_type import TodoType


def _save(session, record):
    if session is not None:
        session.add(record)
        session.commit()


def a_category(session, **kwargs):
    data = dict()
    data["id"] = kwargs.get("id", str(uuid.uuid4()))
    data["user_id"] = kwargs.get("user_id", str(uuid.uuid4()))
    data["name"] = kwargs.get("name", "test")
    data["color"] = kwargs.get("color", "#FFF")

    category_record = Category(**data)

    _save(session, category_record)
    return category_record


def a_habit(session, **kwargs):
    data = dict()
    data["todo_id"] = kwargs.get("todo_id", str(uuid.uuid4()))
    data["todo_owner_id"] = kwargs.get("todo_owner_id", str(uuid.uuid4()))
    data["name"] = kwargs.get("name", "habit")
    data["description"] = kwargs.get("description", "description")
    data["todo_type"] = kwargs.get("todo_type", TodoType.HABIT)
    data["points_per"] = kwargs.get("points_per", 1)
    data["completion_points"] = kwargs.get("completion_points", 1)
    data["frequency"] = kwargs.get("frequency", 1)
    data["period"] = kwargs.get("period", {
        'amount': 1,
        'periodType': 'WEEKS',
        'start': None
    })
    data["buffer"] = kwargs.get("buffer", {
        'amount': 1,
        'bufferType': 'DAY_START'
    })
    data["category"] = kwargs.get("category") or a_category(session)
    data["tags"] = kwargs.get("tags", [])
    data["actions"] = kwargs.get("actions", [])
    data["created_date"] = kwargs.get("created_date", datetime.datetime(2019, 2, 24))
    data["modified_date"] = kwargs.get("modified_date", datetime.datetime(2019, 2, 24))

    habit_record = Habit(**data)

    _save(session, habit_record)
    return habit_record


def a_reoccur(session, **kwargs):
    data = dict()
    data["todo_id"] = kwargs.get("todo_id", str(uuid.uuid4()))
    data["todo_owner_id"] = kwargs.get("todo_owner_id", str(uuid.uuid4()))
    data["name"] = kwargs.get("name", "reoccur")
    data["description"] = kwargs.get("description", "description")
    data["todo_type"] = kwargs.get("todo_type", TodoType.REOCCUR)
    data["completion_points"] = kwargs.get("completion_points", 1)
    data["required"] = kwargs.get("required", False)
    data["repeat"] = kwargs.get("repeat", {
        'when': ["Sunday"],
        'repeatType': 'DAY_OF_WEEK'
    })
    data["category"] = kwargs.get("category") or a_category(session)
    data["tags"] = kwargs.get("tags", [])
    data["actions"] = kwargs.get("actions", [])
    data["created_date"] = kwargs.get("created_date", datetime.datetime(2019, 2, 24))
    data["modified_date"] = kwargs.get("modified_date", datetime.datetime(2019, 2, 24))

    reoccur_record = Reoccur(**data)

    _save(session, reoccur_record)
    return reoccur_record


def a_task(session, **kwargs):
    data = dict()
    data["todo_id"] = kwargs.get("todo_id", str(uuid.uuid4()))
    data["todo_owner_id"] = kwargs.get("todo_owner_id", str(uuid.uuid4()))
    data["name"] = kwargs.get("name", "task")
    data["description"] = kwargs.get("description", "description")
    data["todo_type"] = kwargs.get("todo_type", TodoType.TASK)
    data["completion_points"] = kwargs.get("completion_points", 1)
    data["due_date"] = kwargs.get("due_date")
    data["category"] = kwargs.get("category") or a_category(session)
    data["tags"] = kwargs.get("tags", [])
    data["actions"] = kwargs.get("actions", [])
    data["created_date"] = kwargs.get("created_date", datetime.datetime(2019, 2, 24))
    data["modified_date"] = kwargs.get("modified_date", datetime.datetime(2019, 2, 24))

    task_record = Task(**data)

    _save(session, task_record)
    return task_record


def a_tag(session, **kwargs):
    data = dict()
    data["name"] = kwargs.get("name", "test")

    tag_record = Tag(**data)

    _save(session, tag_record)
    return tag_record


def an_action(session, **kwargs):
    data = dict()
    data["action_date"] = kwargs.get("action_date", datetime.datetime(2019, 2, 24))
    data["points"] = kwargs.get("points", 1)

    action_record = Action(**data)

    _save(session, action_record)
    return action_record

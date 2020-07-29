import datetime
import uuid

from app.model import Category, Habit, Tag, Action, Reoccur, Task
from app.todo.domains.todo_type import TodoType


def a_category(session, **kwargs):
    data = kwargs
    data["id"] = data.get("id", "abc")
    data["name"] = data.get("name", "test")
    data["color"] = data.get("color", "#FFF")

    category_record = Category(**data)

    session.add(category_record)
    session.commit()
    return category_record


def a_habit(session, **kwargs):
    data = kwargs
    data["todo_id"] = data.get("todo_id", str(uuid.uuid4()))
    data["todo_owner_id"] = data.get("todo_owner_id", str(uuid.uuid4()))
    data["name"] = data.get("name", "habit")
    data["description"] = data.get("description", "description")
    data["todo_type"] = data.get("todo_type", TodoType.HABIT)
    data["points_per"] = data.get("points_per", 1)
    data["completion_points"] = data.get("completion_points", 1)
    data["frequency"] = data.get("frequency", 1)
    data["period"] = data.get("period", {
        'amount': 1,
        'periodType': 'WEEKS',
        'start': None
    })
    data["buffer"] = data.get("buffer", {
        'amount': 1,
        'bufferType': 'DAY_START'
    })
    data["category"] = data.get("category", a_category(session))
    data["tags"] = data.get("tags", [])
    data["actions"] = data.get("actions", [])
    data["created_date"] = data.get("created_date", datetime.datetime(2019, 2, 24))
    data["modified_date"] = data.get("modified_date", datetime.datetime(2019, 2, 24))

    habit_record = Habit(**data)

    session.add(habit_record)
    session.commit()
    return habit_record


def a_reoccur(session, **kwargs):
    data = kwargs
    data["todo_id"] = data.get("todo_id", str(uuid.uuid4()))
    data["todo_owner_id"] = data.get("todo_owner_id", str(uuid.uuid4()))
    data["name"] = data.get("name", "reoccur")
    data["description"] = data.get("description", "description")
    data["todo_type"] = data.get("todo_type", TodoType.REOCCUR)
    data["completion_points"] = data.get("completion_points", 1)
    data["required"] = data.get("required", False)
    data["repeat"] = data.get("repeat", {
        'when': ["Sunday"],
        'repeatType': 'DAY_OF_WEEK'
    })
    data["category"] = data.get("category", a_category(session))
    data["tags"] = data.get("tags", [])
    data["actions"] = data.get("actions", [])
    data["created_date"] = data.get("created_date", datetime.datetime(2019, 2, 24))
    data["modified_date"] = data.get("modified_date", datetime.datetime(2019, 2, 24))

    reoccur_record = Reoccur(**data)

    session.add(reoccur_record)
    session.commit()
    return reoccur_record


def a_task(session, **kwargs):
    data = kwargs
    data["todo_id"] = data.get("todo_id", str(uuid.uuid4()))
    data["todo_owner_id"] = data.get("todo_owner_id", str(uuid.uuid4()))
    data["name"] = data.get("name", "task")
    data["description"] = data.get("description", "description")
    data["todo_type"] = data.get("todo_type", TodoType.TASK)
    data["completion_points"] = data.get("completion_points", 1)
    data["due_date"] = data.get("due_date")
    data["category"] = data.get("category", a_category(session))
    data["tags"] = data.get("tags", [])
    data["actions"] = data.get("actions", [])
    data["created_date"] = data.get("created_date", datetime.datetime(2019, 2, 24))
    data["modified_date"] = data.get("modified_date", datetime.datetime(2019, 2, 24))

    task_record = Task(**data)

    session.add(task_record)
    session.commit()
    return task_record


def a_tag(session, **kwargs):
    data = kwargs
    data["name"] = data.get("name", "test")

    tag_record = Tag(**data)

    session.add(tag_record)
    session.commit()
    return tag_record


def an_action(session, **kwargs):
    data = kwargs
    data["action_date"] = data.get("action_date", datetime.datetime(2019, 2, 24))
    data["points"] = data.get("points", 1)

    action_record = Action(**data)

    session.add(action_record)
    session.commit()
    return action_record

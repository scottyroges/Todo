import datetime

from dateutil.tz import tzutc
from freezegun import freeze_time

from app.todo.domains.habit.habit_buffer import HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriodType
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.todo_type import TodoType
from app.todo.todo_factory import TodoFactory
from app.utils import make


@freeze_time("2019-02-24")
def test_create_todo_habit():
    todo_data = {
        "name": "habit",
        "todoOwnerId": "123",
        "description": "description",
        "pointsPer": 1,
        "completionPoints": 1,
        "frequency": 1,
        "buffer": {
            "bufferType": "DAY_START",
            "amount": 1
        },
        "period": {
            "periodType": "WEEKS",
            "amount": 1
        },
        "category": {
            "id": "abc",
            "name": "test",
            "color": "#FFF"
        },
        "tags": ["who", "knows"]
    }

    # make.a_category()
    todo_type = TodoType.HABIT
    todo = TodoFactory.create_todo(todo_data, todo_type)

    assert todo.todo_id is not None
    assert todo.name == "habit"
    assert todo.todo_owner.owner_id == "123"
    assert todo.description == "description"
    assert todo.todo_type == TodoType.HABIT
    assert todo.points_per == 1
    assert todo.completion_points == 1
    assert todo.frequency == 1
    assert todo.buffer.buffer_type == HabitBufferType.DAY_START
    assert todo.buffer.amount == 1
    assert todo.period.period_type == HabitPeriodType.WEEKS
    assert todo.period.amount == 1
    assert todo.category.category_id == "abc"
    for tag in todo.tags:
        assert tag.name in ["who", "knows"]
    assert todo.actions == []
    assert todo.created_date == datetime.datetime(2019, 2, 24)
    assert todo.modified_date == datetime.datetime(2019, 2, 24)


@freeze_time("2019-02-24")
def test_create_todo_reoccur():
    todo_data = {
        "name": "reoccur",
        "todoOwnerId": "123",
        "description": "description",
        "completionPoints": 1,
        "required": False,
        "repeat": {
            "repeatType": "DAY_OF_WEEK",
            "when": ["Sunday"]
        },
        "category": {
            "id": "abc",
            "name": "test",
            "color": "#FFF"
        },
        "tags": ["who", "knows"]
    }
    todo_type = TodoType.REOCCUR
    todo = TodoFactory.create_todo(todo_data, todo_type)

    assert todo.todo_id is not None
    assert todo.name == "reoccur"
    assert todo.todo_owner.owner_id == "123"
    assert todo.description == "description"
    assert todo.todo_type == TodoType.REOCCUR
    assert todo.completion_points == 1
    assert todo.required is False
    assert todo.repeat.repeat_type == ReoccurRepeatType.DAY_OF_WEEK
    assert todo.repeat.when == ["Sunday"]
    assert todo.category.category_id == "abc"
    for tag in todo.tags:
        assert tag.name in ["who", "knows"]
    assert todo.actions == []
    assert todo.created_date == datetime.datetime(2019, 2, 24)
    assert todo.modified_date == datetime.datetime(2019, 2, 24)


@freeze_time("2019-02-24")
def test_create_todo_task():
    todo_data = {
        "name": "task",
        "todoOwnerId": "123",
        "description": "description",
        "completionPoints": 1,
        "dueDate": "2019-03-03 00:03:05",
        "category": {
            "id": "abc",
            "name": "test",
            "color": "#FFF"
        },
        "tags": ["who", "knows"]
    }
    todo_type = TodoType.TASK
    todo = TodoFactory.create_todo(todo_data, todo_type)

    assert todo.todo_id is not None
    assert todo.name == "task"
    assert todo.todo_owner.owner_id == "123"
    assert todo.description == "description"
    assert todo.todo_type == TodoType.TASK
    assert todo.completion_points == 1
    assert todo.due_date == datetime.datetime(2019, 3, 3, 0, 3, 5, tzinfo=tzutc())
    assert todo.category.category_id == "abc"
    for tag in todo.tags:
        assert tag.name in ["who", "knows"]
    assert todo.actions == []
    assert todo.created_date == datetime.datetime(2019, 2, 24)
    assert todo.modified_date == datetime.datetime(2019, 2, 24)

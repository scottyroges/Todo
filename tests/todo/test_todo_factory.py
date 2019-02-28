import datetime

from freezegun import freeze_time

from app.todo.domains.habit.habit_buffer import HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriodType
from app.todo.domains.todo_type import TodoType
from app.todo.todo_factory import TodoFactory


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
        "categories": ["test", "again"],
        "tags": ["who", "knows"]
    }
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
    for category in todo.categories:
        assert category.name in ["test", "again"]
    for tag in todo.tags:
        assert tag.name in ["who", "knows"]
    assert todo.actions == []
    assert todo.created_date == datetime.datetime(2019, 2, 24)
    assert todo.modified_date == datetime.datetime(2019, 2, 24)


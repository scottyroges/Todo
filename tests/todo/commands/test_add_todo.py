import datetime
import pytest
from dateutil.tz import tzutc
from freezegun import freeze_time

from app.errors import UnauthorizedError
from app.todo.domains.habit.habit_buffer import HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriodType
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeatType
from app.todo.domains.todo_type import TodoType
from app.todo.commands.add_todo import AddTodo


class TestAddTodoHabit:
    @freeze_time("2019-02-24")
    def test_add_todo_habit(self, user_request, todo_repo):
        todo_data = {
            "name": "habit",
            "todoOwnerId": user_request.user_id,
            "description": "description",
            "todoType": "HABIT",
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
        todo = AddTodo().execute(todo_data)

        assert todo.todo_id is not None
        assert todo.name == "habit"
        assert todo.todo_owner.owner_id == user_request.user_id
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

    def test_add_todo_unauthorized(self, user_request):
        todo_data = {
            "name": "habit",
            "todo_owner_id": "456",
            "description": "description",
            "todoType": "HABIT",
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

        with pytest.raises(UnauthorizedError):
            AddTodo().execute(todo_data)


class TestAddTodoReoccur:
    @freeze_time("2019-02-24")
    def test_add_todo_reoccur(self, user_request, todo_repo):
        todo_data = {
            "name": "reoccur",
            "todoOwnerId": user_request.user_id,
            "description": "description",
            "todoType": "REOCCUR",
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
        todo = AddTodo().execute(todo_data)

        assert todo.todo_id is not None
        assert todo.name == "reoccur"
        assert todo.todo_owner.owner_id == user_request.user_id
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

    def test_add_todo_unauthorized(self, user_request):
        todo_data = {
            "name": "reoccur",
            "todoOwnerId": "456",
            "description": "description",
            "todoType": "REOCCUR",
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

        with pytest.raises(UnauthorizedError):
            AddTodo().execute(todo_data)


class TestAddTodoTask:
    @freeze_time("2019-02-24")
    def test_add_todo_task(self, user_request, todo_repo):
        todo_data = {
            "name": "task",
            "todoOwnerId": user_request.user_id,
            "description": "description",
            "todoType": "TASK",
            "completionPoints": 1,
            "dueDate": "2019-03-03 00:20:05",
            "category": {
                "id": "abc",
                "name": "test",
                "color": "#FFF"
            },
            "tags": ["who", "knows"]
        }
        todo = AddTodo().execute(todo_data)

        assert todo.todo_id is not None
        assert todo.name == "task"
        assert todo.todo_owner.owner_id == user_request.user_id
        assert todo.description == "description"
        assert todo.todo_type == TodoType.TASK
        assert todo.completion_points == 1
        assert todo.due_date == datetime.datetime(2019, 3, 3, 0, 20, 5, tzinfo=tzutc())
        assert todo.category.category_id == "abc"
        for tag in todo.tags:
            assert tag.name in ["who", "knows"]
        assert todo.actions == []
        assert todo.created_date == datetime.datetime(2019, 2, 24)
        assert todo.modified_date == datetime.datetime(2019, 2, 24)

    def test_add_todo_unauthorized(self, user_request):
        todo_data = {
            "name": "task",
            "todoOwnerId": "456",
            "description": "description",
            "todoType": "TASK",
            "completionPoints": 1,
            "dueDate": "2019-03-03 00:20:05",
            "category": {
                "id": "abc",
                "name": "test",
                "color": "#FFF"
            },
            "tags": ["who", "knows"]
        }

        with pytest.raises(UnauthorizedError):
            AddTodo().execute(todo_data)

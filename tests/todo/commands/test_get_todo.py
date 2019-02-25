import pytest
from freezegun import freeze_time

from app.errors import UnauthorizedError, NotFoundError
from app.todo.domains.action import Action
from app.todo.domains.category import Category
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBuffer, HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.tag import Tag
from app.todo.domains.todo_owner import TodoOwner
from app.todo.commands.get_todo import GetTodo


def _create_habit():
    todo_owner = TodoOwner(owner_id="123")
    period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                         amount=1,
                         start=None)
    buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                         amount=1)
    categories = [Category(name="test"), Category(name="again")]
    tags = [Tag(name="who"), Tag(name="knows")]
    actions = [Action()]
    habit = Habit(todo_id="abc",
                  todo_owner=todo_owner,
                  name="habit",
                  description="description",
                  points_per=1,
                  completion_points=1,
                  frequency=1,
                  period=period,
                  buffer=buffer,
                  categories=categories,
                  tags=tags,
                  actions=actions)
    return habit


@freeze_time("2019-02-24")
def test_get_todo_habit(user_request, todo_repo):
    habit = _create_habit()
    todo_repo.add(habit)

    todo = GetTodo().execute(todo_id="abc")

    assert todo is not None
    assert todo.todo_id == "abc"


def test_get_todo_unauthorized(user_request, todo_repo):
    habit = _create_habit()
    habit.todo_owner.owner_id = "456"
    todo_repo.add(habit)

    with pytest.raises(UnauthorizedError):
        GetTodo().execute(todo_id="abc")


def test_get_todo_not_found(todo_repo):
    with pytest.raises(NotFoundError):
        GetTodo().execute(todo_id="def")

import datetime

from freezegun import freeze_time

import tests.fake_models
from app.todo.commands.perform_action import PerformAction
from app.todo.domains.category import Category
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBufferType, HabitBuffer
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.tag import Tag
from app.todo.domains.todo_owner import TodoOwner


def _create_habit():
    todo_owner = TodoOwner(owner_id="123")
    period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                         amount=1,
                         start=None)
    buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                         amount=1)
    categories = [Category(name="test"), Category(name="again")]
    tags = [Tag(name="who"), Tag(name="knows")]
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
                  tags=tags)
    return habit


def test_perform_action_on_habit(user_request, todo_repo):
    orig_habit = _create_habit()
    assert len(orig_habit.actions) == 0
    todo_repo.add(orig_habit)

    action_data = {
        "actionDate": "2019-02-21 12:02:05",
        "points": 1,
        "todoId": "abc"
    }

    habit = PerformAction().execute(action_data=action_data)
    assert len(habit.actions) == 1
    assert habit.actions[0].points == 1
    assert habit.actions[0].action_date == datetime.datetime(2019, 2, 21, 12, 2, 5)


@freeze_time("2019-02-24 10:00:04")
def test_perform_action_on_habit_no_date(user_request, todo_repo):
    orig_habit = _create_habit()
    assert len(orig_habit.actions) == 0
    todo_repo.add(orig_habit)

    action_data = {
        "points": 1,
        "todoId": "abc"
    }

    habit = PerformAction().execute(action_data=action_data)
    assert len(habit.actions) == 1
    assert habit.actions[0].points == 1
    assert habit.actions[0].action_date == datetime.datetime(2019, 2, 24, 10, 0, 4)

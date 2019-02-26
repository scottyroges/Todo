import datetime

from freezegun import freeze_time

from app.todo.domains.action import Action
from app.todo.domains.category import Category
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBufferType, HabitBuffer
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.tag import Tag
from app.todo.domains.todo_owner import TodoOwner


@freeze_time("2019-02-24 10:00:04")
def test_to_dict():
    todo_owner = TodoOwner(owner_id="123")
    period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                         amount=1,
                         start=None)
    buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                         amount=1)
    categories = [Category(name="test"), Category(name="again")]
    tags = [Tag(name="who"), Tag(name="knows")]
    actions = [Action(points=2)]
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

    assert habit.to_dict() == {
            "todoId": "abc",
            "todoOwnerId": "123",
            "name": "habit",
            "description": "description",
            "todoType": "HABIT",
            "pointsPer": 1,
            "completionPoints": 1,
            "frequency": 1,
            "period": {
                "periodType": "WEEKS",
                "amount": 1,
                "start": None
            },
            "buffer": {
                "bufferType": "DAY_START",
                "amount": 1,
            },
            "categories": ["test", "again"],
            "tags": ["who", "knows"],
            "createdDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
            "modifiedDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
            "actions": [{
                "actionDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
                "points": 2
            }]
        }
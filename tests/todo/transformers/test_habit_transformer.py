import datetime

from freezegun import freeze_time
from app.model import (
    Habit as HabitRecord,
    Category as CategoryRecord,
    Tag as TagRecord,
    Action as ActionRecord
)
from app.todo.domains.action import Action as DomainAction
from app.todo.domains.category import Category as DomainCategory
from app.todo.domains.habit.habit import Habit as DomainHabit
from app.todo.domains.habit.habit_buffer import HabitBufferType, HabitBuffer
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.tag import Tag as DomainTag
from app.todo.domains.todo_owner import TodoOwner
from app.todo.domains.todo_type import TodoType
from app.todo.transformers.habit_transformer import HabitTransformer


@freeze_time("2019-02-24")
def test_to_record():
    todo_owner = TodoOwner(owner_id="123")
    period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                         amount=1,
                         start=None)
    buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                         amount=1)
    categories = [DomainCategory(name="test"), DomainCategory(name="again")]
    tags = [DomainTag(name="who"), DomainTag(name="knows")]
    actions = [DomainAction()]
    habit = DomainHabit(todo_id="abc",
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

    habit_record = HabitTransformer.to_record(habit)

    assert habit_record.todo_id == habit.todo_id
    assert habit_record.todo_owner_id == habit.todo_owner.owner_id
    assert habit_record.name == habit.name
    assert habit_record.description == habit.description
    assert habit_record.points_per == habit.points_per
    assert habit_record.completion_points == habit.completion_points
    assert habit_record.frequency == habit.frequency
    assert habit_record.period == {
        'amount': 1,
        'periodType': 'WEEKS',
        'start': None
    }
    assert habit_record.buffer == {
        'amount': 1,
        'bufferType': 'DAY_START'
    }
    for category_record in habit_record.categories:
        category = filter(lambda x: x.name == category_record.name, habit.categories)
        assert category is not None
    for tag_record in habit_record.tags:
        tag = filter(lambda x: x.name == tag_record.name, habit.tags)
        assert tag is not None
    assert habit_record.actions[0].points == habit.actions[0].points
    assert habit_record.actions[0].action_date == habit.actions[0].action_date
    assert habit_record.created_date == habit.created_date
    assert habit_record.modified_date == habit.modified_date


def test_from_record():
    period = {
        'amount': 1,
        'periodType': 'WEEKS',
        'start': None
    }
    buffer = {
        'amount': 1,
        'bufferType': 'DAY_START'
    }
    categories = [CategoryRecord(name="test"), CategoryRecord(name="again")]
    tags = [TagRecord(name="who"), TagRecord(name="knows")]
    actions = [ActionRecord(action_date=datetime.datetime(2019, 2, 24),
                            points=1)]
    habit_record = HabitRecord(todo_id="abc",
                               todo_owner_id="123",
                               name="habit",
                               description="description",
                               todo_type=TodoType.HABIT,
                               points_per=1,
                               completion_points=1,
                               frequency=1,
                               period=period,
                               buffer=buffer,
                               categories=categories,
                               tags=tags,
                               actions=actions,
                               created_date=datetime.datetime(2019, 2, 24),
                               modified_date=datetime.datetime(2019, 2, 24))

    habit = HabitTransformer.from_record(habit_record)

    assert habit.todo_id == habit_record.todo_id
    assert habit.todo_owner.owner_id == habit_record.todo_owner_id
    assert habit.name == habit_record.name
    assert habit.description == habit_record.description
    assert habit.points_per == habit_record.points_per
    assert habit.completion_points == habit_record.completion_points
    assert habit.frequency == habit_record.frequency
    assert habit.period.amount == 1
    assert habit.period.period_type == HabitPeriodType.WEEKS
    assert habit.period.start is None
    assert habit.buffer.amount == 1
    assert habit.buffer.buffer_type == HabitBufferType.DAY_START
    for category in habit.categories:
        category_record = filter(lambda x: x.name == category.name, habit_record.categories)
        assert category_record is not None
    for tag in habit.tags:
        tag_record = filter(lambda x: x.name == tag.name, habit_record.tags)
        assert tag_record is not None
    assert habit.actions[0].points == habit_record.actions[0].points
    assert habit.actions[0].action_date == habit_record.actions[0].action_date
    assert habit.created_date == habit_record.created_date
    assert habit.modified_date == habit_record.modified_date

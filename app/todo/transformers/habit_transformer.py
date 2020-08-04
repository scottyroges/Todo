from app.model import (
    Action as ActionRecord,
    Category as CategoryRecord,
    Habit as HabitRecord,
    Tag as TagRecord
)
from app.todo.domains.action import Action as DomainAction
from app.todo.domains.habit.habit import Habit as DomainHabit
from app.todo.domains.category import Category as DomainCategory
from app.todo.domains.tag import Tag as DomainTag
from app.todo.domains.habit.habit_buffer import HabitBuffer, HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.todo_owner import TodoOwner


class HabitTransformer:
    @classmethod
    def to_record(cls, habit: DomainHabit):
        period = {
            "periodType": habit.period.period_type.name,
            "amount": habit.period.amount
        }

        buffer = {
            "bufferType": habit.buffer.buffer_type.name,
            "amount": habit.buffer.amount
        }

        tags = [TagRecord(id=tag.tag_id,
                          name=tag.name)
                for tag in habit.tags]

        actions = [ActionRecord(id=action.action_id,
                                action_date=action.action_date,
                                points=action.points)
                   for action in habit.actions]

        category_id = habit.category.category_id if habit.category else None

        return HabitRecord(todo_id=habit.todo_id,
                           todo_owner_id=habit.todo_owner.owner_id,
                           name=habit.name,
                           description=habit.description,
                           todo_type=habit.todo_type,
                           points_per=habit.points_per,
                           completion_points=habit.completion_points,
                           frequency=habit.frequency,
                           period=period,
                           buffer=buffer,
                           category_id=category_id,
                           tags=tags,
                           actions=actions,
                           created_date=habit.created_date,
                           modified_date=habit.modified_date)

    @classmethod
    def from_record(cls, habit_record: HabitRecord):
        todo_owner = TodoOwner(owner_id=habit_record.todo_owner_id)
        period = HabitPeriod(period_type=HabitPeriodType[habit_record.period.get("periodType")],
                             amount=habit_record.period.get("amount"))
        buffer = HabitBuffer(buffer_type=HabitBufferType[habit_record.buffer.get("bufferType")],
                             amount=habit_record.buffer.get("amount"))
        category = None
        if habit_record.category:
            category = DomainCategory(category_id=habit_record.category.id,
                                      name=habit_record.category.name,
                                      color=habit_record.category.color)
        tags = [DomainTag(tag_id=tag.id,
                          name=tag.name)
                for tag in habit_record.tags]

        actions = [DomainAction(action_id=action.id,
                                action_date=action.action_date,
                                points=action.points)
                   for action in habit_record.actions]
        return DomainHabit(todo_id=habit_record.todo_id,
                           todo_owner=todo_owner,
                           name=habit_record.name,
                           description=habit_record.description,
                           points_per=habit_record.points_per,
                           completion_points=habit_record.completion_points,
                           frequency=habit_record.frequency,
                           period=period,
                           buffer=buffer,
                           category=category,
                           tags=tags,
                           actions=actions,
                           created_date=habit_record.created_date,
                           modified_date=habit_record.modified_date)

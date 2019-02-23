from app.model.action import Action
from app.model.category import Category
from app.model.habit import Habit
from app.model.tag import Tag
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
            "amount": habit.period.amount,
            "start": habit.period.start
        }

        buffer = {
            "bufferType": habit.buffer.buffer_type.name,
            "amount": habit.buffer.amount
        }

        categories = [Category(id=category.category_id,
                               name=category.name)
                      for category in habit.categories]

        tags = [Tag(id=tag.tag_id,
                    name=tag.name)
                for tag in habit.tags]

        actions = [Action(id=action.action_id,
                          action_date=action.action_date,
                          points=action.points)
                   for action in habit.actions]

        return Habit(todo_id=habit.todo_id,
                     todo_owner_id=habit.todo_owner.owner_id,
                     name=habit.name,
                     description=habit.description,
                     todo_type=habit.todo_type,
                     points_per=habit.points_per,
                     completion_points=habit.completion_points,
                     frequency=habit.frequency,
                     period=period,
                     buffer=buffer,
                     categories=categories,
                     tags=tags,
                     actions=actions,
                     created_date=habit.created_date,
                     modified_date=habit.modified_date)

    @classmethod
    def from_record(cls, habit_record: Habit):
        todo_owner = TodoOwner(owner_id=habit_record.todo_owner_id)
        period = HabitPeriod(period_type=HabitPeriodType[habit_record.period.get("periodType")],
                             amount=habit_record.period.get("amount"),
                             start=habit_record.period.get("start"))
        buffer = HabitBuffer(buffer_type=HabitBufferType[habit_record.buffer.get("bufferType")],
                             amount=habit_record.buffer.get("amount"))
        categories = [DomainCategory(category_id=category.id,
                                     name=category.name)
                      for category in habit_record.categories]
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
                           categories=categories,
                           tags=tags,
                           actions=actions,
                           created_date=habit_record.created_date,
                           modified_date=habit_record.modified_date)

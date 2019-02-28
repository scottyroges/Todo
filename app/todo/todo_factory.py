from app.todo.domains.category import Category
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBuffer, HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.tag import Tag
from app.todo.domains.todo_owner import TodoOwner
from app.todo.domains.todo_type import TodoType


class TodoFactory:
    @classmethod
    def create_todo(cls, todo_data, todo_type):
        if todo_type == TodoType.HABIT:
            return cls.create_habit(todo_data)
        else:
            print("wtf")

    @classmethod
    def create_habit(cls, habit_data):
        todo_owner = TodoOwner(owner_id=habit_data.get("todoOwnerId"))

        period_data = habit_data.get('period')
        period = HabitPeriod(period_type=HabitPeriodType[period_data.get("periodType")],
                             amount=period_data.get("amount"),
                             start=period_data.get("start"))

        buffer_data = habit_data.get('buffer')
        buffer = HabitBuffer(buffer_type=HabitBufferType[buffer_data.get("bufferType")],
                             amount=buffer_data.get("amount"))

        habit = Habit(todo_owner=todo_owner,
                      name=habit_data.get('name'),
                      description=habit_data.get('description'),
                      points_per=habit_data.get('pointsPer'),
                      completion_points=habit_data.get('completionPoints'),
                      frequency=habit_data.get('frequency'),
                      period=period,
                      buffer=buffer)

        categories_data = habit_data.get("categories", [])
        for category_name in categories_data:
            habit.add_category(Category(name=category_name))

        tags_data = habit_data.get("tags", [])
        for tag_name in tags_data:
            habit.add_tag(Tag(name=tag_name))

        return habit

from app.todo.domains.habit import Habit
from app.todo.domains.habit_buffer import HabitBuffer, HabitBufferType
from app.todo.domains.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.todo_type import TodoType


class TodoFactory:
    @classmethod
    def create_todo(cls, todo_data, todo_type):
        if todo_type == TodoType.HABIT.value:
            return cls.create_habit(todo_data)
        else:
            print("wtf")

    @classmethod
    def create_habit(cls, habit_data):
        period_data = habit_data.get('period')
        period = HabitPeriod(period_type=HabitPeriodType[period_data.get("periodType")],
                             amount=period_data.get("amount"),
                             start=period_data.get("start"))

        buffer_data = habit_data.get('buffer')
        buffer = HabitBuffer(buffer_type=HabitBufferType[buffer_data.get("bufferType")],
                             amount=buffer_data.get("amount"))

        return Habit(name=habit_data.get('name'),
                     description=habit_data.get('description'),
                     completion_points=habit_data.get('completionPoints'),
                     frequency=habit_data.get('frequency'),
                     period=period,
                     buffer=buffer,
                     points_per=habit_data.get('points_per'))

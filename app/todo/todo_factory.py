import datetime

from app.todo.domains.category import Category
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBuffer, HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.reoccur.reoccur import Reoccur
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.tag import Tag
from app.todo.domains.task.task import Task
from app.todo.domains.todo_owner import TodoOwner
from app.todo.domains.todo_type import TodoType


class TodoFactory:
    @classmethod
    def create_todo(cls, todo_data, todo_type):
        todo_owner = TodoOwner(owner_id=todo_data.get("todoOwnerId"))

        if todo_type == TodoType.HABIT:
            todo = cls.create_habit(todo_owner, todo_data)
        elif todo_type == TodoType.REOCCUR:
            todo = cls.create_reoccur(todo_owner, todo_data)
        elif todo_type == TodoType.TASK:
            todo = cls.create_task(todo_owner, todo_data)
        else:
            print("wtf")

        # categories_data = todo_data.get("categories", [])
        # for category_name in categories_data:
        #     todo.add_category(Category(name=category_name))

        category_data = todo_data.get("category")
        todo.category = Category(
            category_id=category_data.get("id"),
            name=category_data.get("name"),
            color=category_data.get("color")
        )

        tags_data = todo_data.get("tags", [])
        for tag_name in tags_data:
            todo.add_tag(Tag(name=tag_name))

        return todo

    @classmethod
    def create_habit(cls, todo_owner, habit_data):
        period_data = habit_data.get('period')
        period = HabitPeriod(period_type=HabitPeriodType[period_data.get("periodType")],
                             amount=period_data.get("amount"))

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
        return habit

    @classmethod
    def create_reoccur(cls, todo_owner, reoccur_data):
        repeat_data = reoccur_data.get('repeat')
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType[repeat_data.get("repeatType")],
                               when=repeat_data.get("when"))
        reoccur = Reoccur(todo_owner=todo_owner,
                          name=reoccur_data.get('name'),
                          description=reoccur_data.get('description'),
                          completion_points=reoccur_data.get('completionPoints'),
                          repeat=repeat,
                          required=reoccur_data.get("required"))
        return reoccur

    @classmethod
    def create_task(cls, todo_owner, task_data):
        due_date = None
        if task_data.get("dueDate"):
            due_date = datetime.datetime.strptime(
                task_data.get("dueDate"),
                '%Y-%m-%d %H:%M:%S')
        task = Task(todo_owner=todo_owner,
                    name=task_data.get('name'),
                    description=task_data.get('description'),
                    completion_points=task_data.get('completionPoints'),
                    due_date=due_date)
        return task

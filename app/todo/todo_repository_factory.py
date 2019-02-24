from app.todo.adpaters.sqlalchemy.habit_repository import HabitRepository
from app.todo.adpaters.sqlalchemy.todo_repository import TodoRepository
from app.todo.domains.todo_type import TodoType


class TodoRepositoryFactory:
    @classmethod
    def create(cls, todo=None):
        if todo is None:
            return TodoRepository()

        if todo.todo_type == TodoType.HABIT:
            return HabitRepository()

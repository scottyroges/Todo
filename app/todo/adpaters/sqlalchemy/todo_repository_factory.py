from app.todo.adpaters.sqlalchemy.habit_repository import HabitRepository
from app.todo.domains.todo_type import TodoType


class TodoRepositoryFactory:
    @classmethod
    def create(cls, todo):
        if todo.todo_type == TodoType.HABIT:
            return HabitRepository()

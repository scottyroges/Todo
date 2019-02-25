from app.model import Habit
from app.todo.adpaters.sqlalchemy.habit_repository import HabitRepository
from app.todo.adpaters.sqlalchemy.todo_repository import TodoRepository
from app.todo.todo_repository_factory import TodoRepositoryFactory


def test_create_habit():
    habit = Habit()
    repo = TodoRepositoryFactory.create(habit)
    assert type(repo) == HabitRepository


def test_create_no_todo():
    repo = TodoRepositoryFactory.create()
    assert type(repo) == TodoRepository

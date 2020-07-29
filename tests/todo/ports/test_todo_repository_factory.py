from app.todo.adpaters.sqlalchemy.todo_repository import TodoRepository
from app.todo.ports.todo_repository_factory import TodoRepositoryFactory


def test_create():
    repo = TodoRepositoryFactory.create()
    assert type(repo) == TodoRepository

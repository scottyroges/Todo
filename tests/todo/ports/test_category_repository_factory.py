from app.todo.adpaters.sqlalchemy.category_repository import CategoryRepository
from app.todo.ports.category_repository_factory import CategoryRepositoryFactory


def test_create():
    repo = CategoryRepositoryFactory.create()
    assert type(repo) == CategoryRepository

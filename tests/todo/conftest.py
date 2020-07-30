import pytest


@pytest.fixture()
def todo_repo(mocker):
    repo = TestTodoRepository()
    mock_repo = mocker.patch("app.todo.ports.todo_repository_factory.TodoRepositoryFactory.create")
    mock_repo.return_value = repo
    return repo


class TestTodoRepository:
    def __init__(self, todos=None):
        self.todos = todos or []

    def read(self, todo_id):
        for todo in self.todos:
            if todo.todo_id == todo_id:
                return todo
        return None

    def read_all(self, user_id):
        return list(filter(lambda x: x.todo_owner.owner_id == user_id,
                           self.todos))

    def add(self, todo):
        self.todos.append(todo)
        return todo

    def update(self, todo):
        return todo


@pytest.fixture()
def category_repo(mocker):
    repo = TestCategoryRepository()
    mock_repo = mocker.patch("app.todo.ports.category_repository_factory.CategoryRepositoryFactory.create")
    mock_repo.return_value = repo
    return repo


class TestCategoryRepository:
    def __init__(self, categories=None):
        self.categories = categories or []

    def add(self, category):
        self.categories.append(category)
        return category

    def read_all(self, user_id):
        return list(filter(lambda x: x.user_id == user_id,
                           self.categories))

    def read(self, category_id):
        for category in self.categories:
            if category.id == category_id:
                return category
        return None

    def update(self, category):
        return category


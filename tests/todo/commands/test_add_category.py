import pytest

from app.errors import UnauthorizedError
from app.todo.commands.add_category import AddCategory


class TestAddCategory:
    def test_add_category(self, user_request, category_repo):
        category_data = {
            "userId": "123",
            "name": "test",
            "color": "#FFF"
        }
        category = AddCategory().execute(category_data)

        assert category.category_id is not None
        assert category.user_id == user_request.user_id
        assert category.name == "test"
        assert category.color == "#FFF"

    def test_add_todo_unauthorized(self, user_request):
        category_data = {
            "userId": "456",
            "name": "test",
            "color": "#FFF"
        }
        with pytest.raises(UnauthorizedError):
            AddCategory().execute(category_data)

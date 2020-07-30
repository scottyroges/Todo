import pytest

from app.errors import UnauthorizedError
from app.todo.commands.update_category import UpdateCategory
from app.utils import make


class TestUpdateCategory:
    def test_update_category(self, user_request, category_repo):
        category = category_repo.add(make.a_category(session=None,
                                                     user_id=user_request.get("user_id"),
                                                     color="#b4b4b4"))

        category_data = {
            "id": category.id,
            "name": "test",
            "color": "#ccddff"
        }

        updated_category = UpdateCategory().execute(category_data)

        assert updated_category.category_id == category.id
        assert updated_category.user_id == category.user_id
        assert updated_category.name == category_data["name"]
        assert updated_category.color == category_data["color"]

    def test_update_category_unauthorized(self, user_request, category_repo):
        category = category_repo.add(make.a_category(session=None,
                                                     user_id="456",
                                                     color="#b4b4b4"))

        category_data = {
            "id": category.id,
            "name": "test",
            "color": "#ccddff"
        }

        with pytest.raises(UnauthorizedError):
            UpdateCategory().execute(category_data)

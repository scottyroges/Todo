from app.todo.commands.get_categories import GetCategories
from app.utils import make


class TestGetCategories:
    def test_get_categories(self, category_repo):
        category_repo.add(make.a_category(session=None, user_id="123"))
        category_repo.add(make.a_category(session=None, user_id="456"))
        category_repo.add(make.a_category(session=None, user_id="123"))

        categories = GetCategories().execute("123")

        assert len(categories) == 2

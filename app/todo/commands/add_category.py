from app.auth.auth_util import is_owner_or_admin
from app.errors import UnauthorizedError
from app.todo.domains.category import Category
from app.todo.ports.category_repository_factory import CategoryRepositoryFactory


class AddCategory:
    def execute(self, category_data):
        if not is_owner_or_admin(category_data.get("userId")):
            raise UnauthorizedError("authorized user does not have permission "
                                    "to create category for specified user")

        category = Category(
            user_id=category_data["userId"],
            name=category_data["name"],
            color=category_data["color"]
        )
        return CategoryRepositoryFactory.create().add(category)

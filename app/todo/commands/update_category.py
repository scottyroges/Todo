from app.auth.auth_util import is_owner_or_admin
from app.errors import UnauthorizedError
from app.todo.domains.category import Category
from app.todo.ports.category_repository_factory import CategoryRepositoryFactory


class UpdateCategory:
    def execute(self, category_data):
        repo = CategoryRepositoryFactory.create()
        read_category = repo.read(category_data["id"])

        if not is_owner_or_admin(read_category.user_id):
            raise UnauthorizedError("authorized user does not have permission "
                                    "to update category for specified user")

        category = Category(
            category_id=category_data["id"],
            user_id=read_category.user_id,
            name=category_data["name"],
            color=category_data["color"]
        )

        return repo.update(category)

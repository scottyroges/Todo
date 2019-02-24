from app.auth.auth_util import is_owner_or_admin
from app.errors import UnauthorizedError
from app.todo.todo_repository_factory import TodoRepositoryFactory
from app.todo.domains.category import Category
from app.todo.domains.tag import Tag
from app.todo.domains.todo_owner import TodoOwner
from app.todo.todo_factory import TodoFactory


class AddTodo:
    def execute(self, todo_data, todo_type):
        if not is_owner_or_admin(todo_data.get("todo_owner_id")):
            raise UnauthorizedError("authorized user does not have permission "
                                    "to create habit for specified user")

        todo = TodoFactory.create_todo(todo_data, todo_type)

        todo_owner = TodoOwner(owner_id=todo_data.get("todo_owner_id"))
        todo.todo_owner = todo_owner

        categories_data = todo_data.get("categories", [])
        for category_name in categories_data:
            todo.add_category(Category(name=category_name))

        tags_data = todo_data.get("tags", [])
        for tag_name in tags_data:
            todo.add_tag(Tag(name=tag_name))

        return TodoRepositoryFactory.create(todo).add(todo)

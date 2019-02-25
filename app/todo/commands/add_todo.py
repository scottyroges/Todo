from app.auth.auth_util import is_owner_or_admin
from app.errors import UnauthorizedError
from app.todo.todo_repository_factory import TodoRepositoryFactory
from app.todo.todo_factory import TodoFactory


class AddTodo:
    def execute(self, todo_data, todo_type):
        if not is_owner_or_admin(todo_data.get("todo_owner_id")):
            raise UnauthorizedError("authorized user does not have permission "
                                    "to create habit for specified user")

        todo = TodoFactory.create_todo(todo_data, todo_type)
        return TodoRepositoryFactory.create(todo).add(todo)

from app.auth.auth_util import is_owner_or_admin
from app.errors import UnauthorizedError
from app.todo.domains.todo_type import TodoType
from app.todo.ports.todo_repository_factory import TodoRepositoryFactory
from app.todo.todo_factory import TodoFactory


class AddTodo:
    def execute(self, todo_data):
        if not is_owner_or_admin(todo_data.get("todoOwnerId")):
            raise UnauthorizedError("authorized user does not have permission "
                                    "to create habit for specified user")

        todo_type = TodoType(todo_data["todoType"].upper())

        todo = TodoFactory.create_todo(todo_data, todo_type)
        return TodoRepositoryFactory.create().add(todo)

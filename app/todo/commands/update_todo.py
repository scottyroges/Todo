from app.auth.auth_util import is_owner_or_admin
from app.errors import UnauthorizedError
from app.todo.domains.todo_type import TodoType
from app.todo.ports.todo_repository_factory import TodoRepositoryFactory
from app.todo.todo_factory import TodoFactory


class UpdateTodo:
    def execute(self, todo_data):
        repo = TodoRepositoryFactory.create()
        read_todo = repo.read(todo_data["todoId"])

        if not is_owner_or_admin(read_todo.todo_owner.owner_id):
            raise UnauthorizedError("authorized user does not have permission "
                                    "to update todo for specified user")

        todo_type = TodoType(todo_data["todoType"].upper())
        todo = TodoFactory.create_todo(todo_data, todo_type)
        todo.todo_owner.owner_id = read_todo.todo_owner.owner_id
        return repo.update(todo)

from app.auth.auth_util import is_owner_or_admin
from app.errors import NotFoundError, UnauthorizedError
from app.todo.adpaters.sqlalchemy.todo_repository import TodoRepository


class GetTodo:
    def execute(self, todo_id):
        repo = TodoRepository()
        todo = repo.read(todo_id)

        if not todo:
            raise NotFoundError("No habit with todo_id %s" % todo_id)

        if not is_owner_or_admin(todo.todo_owner.owner_id):
            raise UnauthorizedError("authorized user does not have permission "
                                    "to habit")

        return todo

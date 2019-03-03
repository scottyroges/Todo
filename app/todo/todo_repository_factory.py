from app.todo.adpaters.sqlalchemy.todo_repository import TodoRepository


class TodoRepositoryFactory:
    @classmethod
    def create(cls):
        return TodoRepository()

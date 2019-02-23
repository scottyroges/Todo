from app.todo.adpaters.sqlalchemy.todo_repository import TodoRepository
from app.todo.adpaters.sqlalchemy.todo_repository_factory import TodoRepositoryFactory
from app.todo.domains.action import Action


class PerformAction:
    def execute(self, action_data):
        repo = TodoRepository()
        todo = repo.read(action_data.get("todoId"))
        action = Action(action_date=action_data.get("actionDate"),
                        points=action_data.get("points"))
        todo.perform_action(action)
        return repo.update(todo)

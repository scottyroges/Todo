import datetime

from app.todo.commands.get_todo import GetTodo
from app.todo.domains.action import Action
from app.todo.todo_repository_factory import TodoRepositoryFactory


class PerformAction:
    def execute(self, action_data):
        todo = GetTodo().execute(action_data.get("todoId"))
        action_date = None
        if action_data.get("actionDate"):
            action_date = datetime.datetime.strptime(action_data.get("actionDate"),
                                                     '%Y-%m-%d %H:%M:%S')
        action = Action(action_date=action_date,
                        points=action_data.get("points"))
        todo.perform_action(action)
        repo = TodoRepositoryFactory.create()
        return repo.update(todo)

from app.todo.domains.todo import Todo
from app.todo.domains.todo_type import TodoType


class Task(Todo):
    def __init__(self,
                 todo_id=None,
                 todo_owner=None,
                 name=None,
                 description=None,
                 completion_points=None,
                 due_date=None,
                 categories=None,
                 tags=None,
                 actions=None,
                 created_date=None,
                 modified_date=None):
        super().__init__(todo_id=todo_id,
                         todo_owner=todo_owner,
                         name=name,
                         description=description,
                         todo_type=TodoType.TASK,
                         categories=categories,
                         completion_points=completion_points,
                         tags=tags,
                         actions=actions,
                         created_date=created_date,
                         modified_date=modified_date)
        self.due_date = due_date

    def to_dict(self):
        todo_dict = super().to_dict()
        todo_dict.update({
            "dueDate": self.due_date
        })
        return todo_dict

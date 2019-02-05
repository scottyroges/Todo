import uuid
from datetime import datetime


class Todo:
    def __init__(self,
                 todo_id=None,
                 todo_owner=None,
                 name=None,
                 description=None,
                 todo_type=None,
                 completion_points=0,
                 actions=[],
                 created_date=datetime.now(),
                 modified_date=datetime.now()):
        self.todo_id = todo_id or uuid.uuid4()
        self.todo_owner = todo_owner
        self.name = name
        self.description = description
        self.todo_type = todo_type
        self.completion_points = completion_points
        self.actions = actions
        self.created_date = created_date
        self.modified_date = modified_date

    def add_action(self, action):
        self.actions.append(action)
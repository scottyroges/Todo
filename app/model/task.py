from app.database import db
from app.model import Todo
from app.todo.domains.todo_type import TodoType


class Task(Todo):
    todo_id = db.Column(db.String(36), db.ForeignKey('todo.todo_id'), primary_key=True)
    due_date = db.Column(db.DateTime)

    __mapper_args__ = {
        'polymorphic_identity': TodoType.TASK,
    }

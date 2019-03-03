from app.database import db
from app.model import Todo
from app.todo.domains.todo_type import TodoType


class Reoccur(Todo):
    todo_id = db.Column(db.String(36), db.ForeignKey('todo.todo_id'), primary_key=True)
    repeat = db.Column(db.JSON)
    required = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': TodoType.REOCCUR,
    }

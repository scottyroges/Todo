from app.model.todo import Todo
from app.database import db
from app.todo.domains.todo_type import TodoType


class Habit(Todo):
    todo_id = db.Column(db.String(36), db.ForeignKey('todo.todo_id'), primary_key=True)
    points_per = db.Column(db.Integer)
    frequency = db.Column(db.Integer)
    period = db.Column(db.JSON)
    buffer = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity': TodoType.HABIT,
    }

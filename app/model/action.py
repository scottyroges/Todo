from app.model.mixins.id_mixin import IdMixin
from app.database import db


class Action(db.Model, IdMixin):
    todo_id = db.Column(db.String(36), db.ForeignKey('todo.todo_id'))
    action_date = db.Column(db.DateTime)
    points = db.Column(db.Integer)

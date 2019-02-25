from app.model.mixins.id_mixin import IdMixin
from app.model.mixins.time_mixin import TimeMixin
from app.database import db


class Tag(db.Model, IdMixin, TimeMixin):
    todo_id = db.Column(db.String(36), db.ForeignKey('todo.todo_id'))
    name = db.Column(db.String)

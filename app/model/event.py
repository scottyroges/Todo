from arrow import Arrow

from app.model.id_mixin import IdMixin
from app.model.time_mixin import TimeMixin
from app.server import db


class Event(db.Model, IdMixin, TimeMixin):
    todo_id = db.Column(db.String(36), db.ForeignKey('habit.id'))
    event_date = db.Column(db.DateTime)
    points = db.Column(db.Integer)

    def save(self):
        self.modified_date = Arrow.now()
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "todoId": self.todo_id,
            "eventDate": self.event_date,
            "points": self.points,
            "created_date": self.created_date,
            "modified_date": self.modified_date
        }

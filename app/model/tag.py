from app.model.id_mixin import IdMixin
from app.model.time_mixin import TimeMixin
from app.server import db


class Tag(db.Model, IdMixin, TimeMixin):
    name = db.Column(db.String)

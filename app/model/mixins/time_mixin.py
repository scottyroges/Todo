from arrow import Arrow

from app.server import db


class TimeMixin(object):
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)

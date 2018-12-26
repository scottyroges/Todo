from arrow import Arrow
from marshmallow import fields

from marshmallow_enum import EnumField

from app.model.joins import todo_category_xref, todo_tag_xref
from app.model.id_mixin import IdMixin
from app.model.schema.smart_nested import SmartNested
from app.model.time_mixin import TimeMixin
from app.server import db
from app.model.todo import TodoType


class Habit(db.Model, IdMixin, TimeMixin):
    # TODO: this can all be moved to a base class (Todo)
    user_id = db.Column(db.String)  # TODO: figure out how this will work with cognito
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    type = db.Column(db.Enum(TodoType))
    default_points = db.Column(db.Integer)
    events = db.relationship("Event")
    categories = db.relationship("Category",
                                 secondary=todo_category_xref)
    tags = db.relationship("Tag",
                           secondary=todo_tag_xref)

    # habit specific
    frequency = db.Column(db.Integer)
    range = db.Column(db.JSON)
    buffer = db.Column(db.JSON)

    __schema_fields__ = {
        "type": EnumField(TodoType, by_name=True),
        "events": fields.Nested('EventSchema', many=True)
    }

    def save(self):
        self.modified_date = Arrow.now()
        db.session.add(self)
        db.session.commit()

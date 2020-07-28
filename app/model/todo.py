from app.model.mixins.time_mixin import TimeMixin
from app.database import db
from app.todo.domains.todo_type import TodoType


class Todo(db.Model, TimeMixin):
    todo_id = db.Column(db.String(36), primary_key=True)
    todo_owner_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    todo_type = db.Column(db.Enum(TodoType))
    completion_points = db.Column(db.Integer)
    # categories = db.relationship("Category", lazy='joined')
    category_id = db.Column(db.String, db.ForeignKey('category.id'))
    category = db.relationship("Category")
    tags = db.relationship("Tag", lazy='joined')
    actions = db.relationship("Action", lazy='joined')

    __mapper_args__ = {
        'polymorphic_identity': 'TODO',
        'polymorphic_on': todo_type
    }

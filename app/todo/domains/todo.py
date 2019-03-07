import uuid
from datetime import datetime

from app.todo.domains.category import Category
from app.todo.domains.tag import Tag


class Todo:
    def __init__(self,
                 todo_id=None,
                 todo_owner=None,
                 name=None,
                 description=None,
                 todo_type=None,
                 completion_points=None,
                 categories=None,
                 tags=None,
                 actions=None,
                 created_date=None,
                 modified_date=None):
        self.todo_id = todo_id or uuid.uuid4()
        self.todo_owner = todo_owner
        self.name = name
        self.description = description
        self.todo_type = todo_type
        self.completion_points = completion_points or 0
        self.categories = categories or []
        self.tags = tags or []
        self.actions = actions or []
        self.created_date = created_date or datetime.now()
        self.modified_date = modified_date or datetime.now()

    def add_category(self, category: Category):
        self.categories.append(category)

    def add_tag(self, tag: Tag):
        self.tags.append(tag)

    def perform_action(self, action):
        self.actions.append(action)

    def to_dict(self):
        return {
            "todoId": self.todo_id,
            "todoOwnerId": self.todo_owner.owner_id,
            "name": self.name,
            "description": self.description,
            "todoType": self.todo_type.name,
            "completionPoints": self.completion_points,
            "categories": [category.name for category in self.categories],
            "tags": [tag.name for tag in self.tags],
            "actions": [action.to_dict() for action in self.actions],
            "createdDate": self.created_date,
            "modifiedDate": self.modified_date,
            "should_show": self.should_show
        }

    @property
    def last_action(self):
        if len(self.actions) == 0:
            return None

        return sorted(self.actions,
                      key=lambda x: x.action_date,
                      reverse=True)[0]

    @property
    def should_show(self):
        # should be overriden by all children
        return True

import uuid


class Category:
    def __init__(self, category_id=None, user_id=None, name=None, color=None):
        self.category_id = category_id or str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.color = color

    def to_dict(self):
        return {
            "id": self.category_id,
            # "user_id": self.user_id,
            "name": self.name,
            "color": self.color
        }

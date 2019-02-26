from app.todo.domains.todo import Todo
from app.todo.domains.todo_type import TodoType


class Habit(Todo):
    def __init__(self,
                 todo_id=None,
                 todo_owner=None,
                 name=None,
                 description=None,
                 points_per=None,
                 completion_points=None,
                 frequency=None,
                 period=None,
                 buffer=None,
                 categories=None,
                 tags=None,
                 actions=None,
                 created_date=None,
                 modified_date=None):
        super().__init__(todo_id=todo_id,
                         todo_owner=todo_owner,
                         name=name,
                         description=description,
                         todo_type=TodoType.HABIT,
                         completion_points=completion_points,
                         categories=categories,
                         tags=tags,
                         actions=actions,
                         created_date=created_date,
                         modified_date=modified_date)
        self.points_per = points_per or 0
        self.frequency = frequency
        self.period = period
        self.buffer = buffer

    def to_dict(self):
        return {
            "todoId": self.todo_id,
            "todoOwnerId": self.todo_owner.owner_id,
            "name": self.name,
            "description": self.description,
            "todoType": self.todo_type.name,
            "pointsPer": self.points_per,
            "completionPoints": self.completion_points,
            "frequency": self.frequency,
            "period": {
                "periodType": self.period.period_type.name,
                "amount": self.period.amount,
                "start": self.period.start
            },
            "buffer": {
                "bufferType": self.buffer.buffer_type.name,
                "amount": self.buffer.amount,
            },
            "categories": [category.name for category in self.categories],
            "tags": [tag.name for tag in self.tags],
            "createdDate": self.created_date,
            "modifiedDate": self.modified_date,
            "actions": [action.to_dict() for action in self.actions]
        }

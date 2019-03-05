import datetime

from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeatType
from app.todo.domains.todo import Todo
from app.todo.domains.todo_type import TodoType


class Reoccur(Todo):
    def __init__(self,
                 todo_id=None,
                 todo_owner=None,
                 name=None,
                 description=None,
                 completion_points=None,
                 repeat=None,
                 required=None,
                 categories=None,
                 tags=None,
                 actions=None,
                 created_date=None,
                 modified_date=None):
        super().__init__(todo_id=todo_id,
                         todo_owner=todo_owner,
                         name=name,
                         description=description,
                         todo_type=TodoType.REOCCUR,
                         categories=categories,
                         completion_points=completion_points,
                         tags=tags,
                         actions=actions,
                         created_date=created_date,
                         modified_date=modified_date)
        self.repeat = repeat
        self.required = required or False

    def to_dict(self):
        todo_dict = super().to_dict()
        todo_dict.update({
            "repeat": {
                "repeatType": self.repeat.repeat_type.name,
                "when": self.repeat.when
            },
            "required": self.required
        })
        return todo_dict

    @property
    def is_complete(self):
        today = datetime.datetime.today().replace(hour=4, minute=0, second=0, microsecond=0)
        if self.repeat.repeat_type == ReoccurRepeatType.DAY_OF_WEEK:
            start = today - datetime.timedelta(days=today.weekday())
        current_actions = [action for action in self.actions
                           if action.action_date > start]
        return False



import calendar
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
    def should_show(self):

        today = datetime.datetime.today()
        if self.repeat.repeat_type == ReoccurRepeatType.DAY_OF_WEEK:
            if self.required:
                days = dict(zip(calendar.day_name, range(7)))
                num_actions_expected = 0
                for when in self.repeat.when:
                    if days[when] <= today.weekday():
                        num_actions_expected += 1

                week_start = today.replace(hour=4, minute=0, second=0, microsecond=0) - datetime.timedelta(days=today.weekday())
                current_actions = [action for action in self.actions
                                   if action.action_date > week_start]

                return len(current_actions) < num_actions_expected

            # repeat day
            if not calendar.day_name[today.weekday()] in self.repeat.when:
                return False

            last_action = self.last_action

            # no actions
            if last_action is None:
                return True

            return self.last_action.action_date.date() != today.date()
        return False



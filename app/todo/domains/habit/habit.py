import calendar
import datetime

from app.todo.domains.habit.habit_buffer import HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriodType
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
        todo_dict = super().to_dict()
        todo_dict.update({
            "pointsPer": self.points_per,
            "frequency": self.frequency,
            "period": {
                "periodType": self.period.period_type.name,
                "amount": self.period.amount
            },
            "buffer": {
                "bufferType": self.buffer.buffer_type.name,
                "amount": self.buffer.amount,
            }
        })
        return todo_dict

    @property
    def is_complete(self):
        # TODO: this our out default start time for daily tasks 4am,
        # i have a feeling this might cause some issues with timezones
        today = datetime.datetime.today().replace(hour=4, minute=0, second=0, microsecond=0)
        if self.period.period_type == HabitPeriodType.DAYS:
            start = today - datetime.timedelta(days=self.period.amount - 1)
        elif self.period.period_type == HabitPeriodType.WEEKS:
            start = today - datetime.timedelta(days=today.weekday())
        elif self.period.period_type == HabitPeriodType.MONTHS:
            start = today - datetime.timedelta(days=today.day-1)
        elif self.period.period_type == HabitPeriodType.YEARS:
            start = today.replace(month=1, day=1)
        current_actions = [action for action in self.actions
                           if action.action_date > start]
        return len(current_actions) >= self.frequency

    @property
    def should_show(self):
        if self.buffer is None or len(self.actions) == 0:
            return True

        if self.is_complete:
            return False

        # TODO: This is not taking into account the start of a period, should it?

        today = datetime.datetime.today()
        last_action = self.last_action

        if self.buffer.buffer_type == HabitBufferType.HOURS:
            buffer_cutoff = last_action.action_date + datetime.timedelta(hours=self.buffer.amount)
        elif self.buffer.buffer_type == HabitBufferType.DAYS:
            buffer_cutoff = last_action.action_date + datetime.timedelta(days=self.buffer.amount)
        elif self.buffer.buffer_type == HabitBufferType.DAY_START:
            current_day_start = last_action.action_date.replace(hour=4, minute=0, second=0, microsecond=0)
            if today < current_day_start:
                current_day_start = current_day_start - datetime.timedelta(days=1)

            buffer_cutoff = current_day_start + datetime.timedelta(days=self.buffer.amount)
        elif self.buffer.buffer_type == HabitBufferType.WEEKS:
            buffer_cutoff = last_action.action_date + datetime.timedelta(days=self.buffer.amount * 7)
        elif self.buffer.buffer_type == HabitBufferType.MONTHS:
            buffer_cutoff = last_action.action_date.replace(month=last_action.action_date.month + self.buffer.amount)

        return today > buffer_cutoff


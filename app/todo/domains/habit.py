from app.todo.domains.todo import Todo
from app.todo.domains.todo_type import TodoType


class Habit(Todo):
    def __init__(self,
                 todo_owner=None,
                 name=None,
                 description=None,
                 points_per=0,
                 completion_points=0,
                 frequency=None,
                 period=None,
                 buffer=None):
        super().__init__(todo_owner,
                         name,
                         description,
                         TodoType.HABIT,
                         completion_points)
        self.points_per = points_per
        self.frequency = frequency
        self.period = period
        self.buffer = buffer

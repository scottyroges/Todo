import datetime

from freezegun import freeze_time

from app.todo.commands.get_todos import GetAllTodos
from app.todo.domains.action import Action
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBufferType, HabitBuffer
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.reoccur.reoccur import Reoccur
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.task.task import Task
from app.todo.domains.todo_owner import TodoOwner


def test_get_todos_all(user_request, todo_repo):
    todo_owner = TodoOwner(owner_id="123")
    period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                         amount=1)
    buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                         amount=1)
    habit = Habit(todo_id="abc",
                  todo_owner=todo_owner,
                  name="habit",
                  description="description",
                  points_per=1,
                  completion_points=1,
                  frequency=1,
                  period=period,
                  buffer=buffer)
    todo_repo.add(habit)

    repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                           when=["Sunday"])
    reoccur = Reoccur(todo_id="abc",
                      todo_owner=todo_owner,
                      name="reoccur",
                      description="description",
                      completion_points=1,
                      required=False,
                      repeat=repeat)
    todo_repo.add(reoccur)

    actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 0, 4))]
    task = Task(todo_id="abc",
                todo_owner=todo_owner,
                name="task",
                description="description",
                completion_points=1,
                due_date=datetime.datetime(2019, 3, 3, 0, 25, 5),
                actions=actions)
    todo_repo.add(task)

    todos = GetAllTodos().execute(user_id=user_request.get("user_id"), only_shows=False)
    assert len(todos) == 3


@freeze_time("2019-03-07")
def test_get_todos_show_habit(user_request, todo_repo):
    todo_owner = TodoOwner(owner_id="123")
    period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                         amount=1)
    buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                         amount=1)
    habit1 = Habit(todo_id="abc",
                   todo_owner=todo_owner,
                   name="habit1",
                   description="description",
                   points_per=1,
                   completion_points=1,
                   frequency=1,
                   period=period,
                   buffer=buffer)
    todo_repo.add(habit1)

    actions = [Action(action_date=datetime.datetime(2019, 3, 5, 11, 0, 4))]
    habit2 = Habit(todo_id="abc",
                   todo_owner=todo_owner,
                   name="habit2",
                   description="description",
                   points_per=1,
                   completion_points=1,
                   frequency=1,
                   period=period,
                   buffer=buffer,
                   actions=actions)
    todo_repo.add(habit2)

    todos = GetAllTodos().execute(user_id=user_request.get("user_id"), only_shows=True)
    assert len(todos) == 1


@freeze_time("2019-03-07")
def test_get_todos_show_reoccur(user_request, todo_repo):
    todo_owner = TodoOwner(owner_id="123")
    repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                           when=["Thursday"])
    reoccur1 = Reoccur(todo_id="abc",
                       todo_owner=todo_owner,
                       name="reoccur",
                       description="description",
                       completion_points=1,
                       required=False,
                       repeat=repeat)
    todo_repo.add(reoccur1)

    actions = [Action(action_date=datetime.datetime(2019, 3, 7, 11, 0, 4))]
    reoccur2 = Reoccur(todo_id="abc",
                       todo_owner=todo_owner,
                       name="reoccur",
                       description="description",
                       completion_points=1,
                       required=False,
                       repeat=repeat,
                       actions=actions)
    todo_repo.add(reoccur2)

    todos = GetAllTodos().execute(user_id=user_request.get("user_id"), only_shows=True)
    assert len(todos) == 1


@freeze_time("2019-03-07")
def test_get_todos_show_task(user_request, todo_repo):
    todo_owner = TodoOwner(owner_id="123")
    task1 = Task(todo_id="abc",
                 todo_owner=todo_owner,
                 name="task",
                 description="description",
                 completion_points=1,
                 due_date=datetime.datetime(2019, 3, 3, 0, 25, 5))
    todo_repo.add(task1)

    actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 0, 4))]
    task2 = Task(todo_id="abc",
                 todo_owner=todo_owner,
                 name="task",
                 description="description",
                 completion_points=1,
                 due_date=datetime.datetime(2019, 3, 3, 0, 25, 5),
                 actions=actions)
    todo_repo.add(task2)

    todos = GetAllTodos().execute(user_id=user_request.get("user_id"), only_shows=True)
    assert len(todos) == 1

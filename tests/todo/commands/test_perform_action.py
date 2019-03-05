import datetime
from freezegun import freeze_time

from app.todo.commands.perform_action import PerformAction
from app.todo.domains.category import Category
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBufferType, HabitBuffer
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.reoccur.reoccur import Reoccur
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeatType, ReoccurRepeat
from app.todo.domains.tag import Tag
from app.todo.domains.task.task import Task
from app.todo.domains.todo_owner import TodoOwner


class TestPerformActionHabit:
    def _create_habit(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                             amount=1)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=1)
        categories = [Category(name="test"), Category(name="again")]
        tags = [Tag(name="who"), Tag(name="knows")]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      buffer=buffer,
                      categories=categories,
                      tags=tags)
        return habit

    def test_perform_action_on_habit(self, user_request, todo_repo):
        orig_habit = self._create_habit()
        assert len(orig_habit.actions) == 0
        todo_repo.add(orig_habit)

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": 1,
            "todoId": "abc"
        }

        habit = PerformAction().execute(action_data=action_data)
        assert len(habit.actions) == 1
        assert habit.actions[0].points == 1
        assert habit.actions[0].action_date == datetime.datetime(2019, 2, 21, 12, 2, 5)

    @freeze_time("2019-02-24 10:00:04")
    def test_perform_action_on_habit_no_date(self, user_request, todo_repo):
        orig_habit = self._create_habit()
        assert len(orig_habit.actions) == 0
        todo_repo.add(orig_habit)

        action_data = {
            "points": 1,
            "todoId": "abc"
        }

        habit = PerformAction().execute(action_data=action_data)
        assert len(habit.actions) == 1
        assert habit.actions[0].points == 1
        assert habit.actions[0].action_date == datetime.datetime(2019, 2, 24, 10, 0, 4)


class TestPerformActionReoccur:
    def _create_reoccur(self):
        todo_owner = TodoOwner(owner_id="123")
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Sunday"])
        categories = [Category(name="test"), Category(name="again")]
        tags = [Tag(name="who"), Tag(name="knows")]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=False,
                          repeat=repeat,
                          categories=categories,
                          tags=tags)
        return reoccur

    def test_perform_action_on_reoccur(self, user_request, todo_repo):
        orig_reoccur = self._create_reoccur()
        assert len(orig_reoccur.actions) == 0
        todo_repo.add(orig_reoccur)

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": 1,
            "todoId": "abc"
        }

        reoccur = PerformAction().execute(action_data=action_data)
        assert len(reoccur.actions) == 1
        assert reoccur.actions[0].points == 1
        assert reoccur.actions[0].action_date == datetime.datetime(2019, 2, 21, 12, 2, 5)

    @freeze_time("2019-02-24 10:00:04")
    def test_perform_action_on_reoccur_no_date(self, user_request, todo_repo):
        orig_reoccur = self._create_reoccur()
        assert len(orig_reoccur.actions) == 0
        todo_repo.add(orig_reoccur)

        action_data = {
            "points": 1,
            "todoId": "abc"
        }

        reoccur = PerformAction().execute(action_data=action_data)
        assert len(reoccur.actions) == 1
        assert reoccur.actions[0].points == 1
        assert reoccur.actions[0].action_date == datetime.datetime(2019, 2, 24, 10, 0, 4)


class TestPerformActionTask:
    def _create_task(self):
        todo_owner = TodoOwner(owner_id="123")
        categories = [Category(name="test"), Category(name="again")]
        tags = [Tag(name="who"), Tag(name="knows")]
        task = Task(todo_id="abc",
                    todo_owner=todo_owner,
                    name="reoccur",
                    description="description",
                    completion_points=1,
                    due_date=datetime.datetime(2019, 3, 3, 0, 29, 5),
                    categories=categories,
                    tags=tags)
        return task

    def test_perform_action_on_task(self, user_request, todo_repo):
        orig_task = self._create_task()
        assert len(orig_task.actions) == 0
        todo_repo.add(orig_task)

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": 1,
            "todoId": "abc"
        }

        task = PerformAction().execute(action_data=action_data)
        assert len(task.actions) == 1
        assert task.actions[0].points == 1
        assert task.actions[0].action_date == datetime.datetime(2019, 2, 21, 12, 2, 5)

    @freeze_time("2019-02-24 10:00:04")
    def test_perform_action_on_reoccur_no_date(self, user_request, todo_repo):
        orig_task = self._create_task()
        assert len(orig_task.actions) == 0
        todo_repo.add(orig_task)

        action_data = {
            "points": 1,
            "todoId": "abc"
        }

        task = PerformAction().execute(action_data=action_data)
        assert len(task.actions) == 1
        assert task.actions[0].points == 1
        assert task.actions[0].action_date == datetime.datetime(2019, 2, 24, 10, 0, 4)

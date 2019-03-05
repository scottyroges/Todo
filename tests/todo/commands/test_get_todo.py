import datetime

import pytest
from freezegun import freeze_time

from app.errors import UnauthorizedError, NotFoundError
from app.todo.domains.action import Action
from app.todo.domains.category import Category
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBuffer, HabitBufferType
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.reoccur.reoccur import Reoccur
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.tag import Tag
from app.todo.domains.task.task import Task
from app.todo.domains.todo_owner import TodoOwner
from app.todo.commands.get_todo import GetTodo


class TestGetTodoHabit:
    def _create_habit(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                             amount=1)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=1)
        categories = [Category(name="test"), Category(name="again")]
        tags = [Tag(name="who"), Tag(name="knows")]
        actions = [Action()]
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
                      tags=tags,
                      actions=actions)
        return habit

    @freeze_time("2019-02-24")
    def test_get_todo_habit(self, user_request, todo_repo):
        habit = self._create_habit()
        todo_repo.add(habit)

        todo = GetTodo().execute(todo_id="abc")

        assert todo is not None
        assert todo.todo_id == "abc"

    def test_get_todo_unauthorized(self, user_request, todo_repo):
        habit = self._create_habit()
        habit.todo_owner.owner_id = "456"
        todo_repo.add(habit)

        with pytest.raises(UnauthorizedError):
            GetTodo().execute(todo_id="abc")

    def test_get_todo_not_found(self, todo_repo):
        with pytest.raises(NotFoundError):
            GetTodo().execute(todo_id="def")


class TestGetTodoReoccur:
    def _create_reoccur(self):
        todo_owner = TodoOwner(owner_id="123")
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Sunday"])
        categories = [Category(name="test"), Category(name="again")]
        tags = [Tag(name="who"), Tag(name="knows")]
        actions = [Action()]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=False,
                          repeat=repeat,
                          categories=categories,
                          tags=tags,
                          actions=actions)
        return reoccur

    @freeze_time("2019-02-24")
    def test_get_todo_reoccur(self, user_request, todo_repo):
        reoccur = self._create_reoccur()
        todo_repo.add(reoccur)

        todo = GetTodo().execute(todo_id="abc")

        assert todo is not None
        assert todo.todo_id == "abc"

    def test_get_todo_unauthorized(self, user_request, todo_repo):
        reoccur = self._create_reoccur()
        reoccur.todo_owner.owner_id = "456"
        todo_repo.add(reoccur)

        with pytest.raises(UnauthorizedError):
            GetTodo().execute(todo_id="abc")

    def test_get_todo_not_found(self, todo_repo):
        with pytest.raises(NotFoundError):
            GetTodo().execute(todo_id="def")


class TestGetTodoTask:
    def _create_task(self):
        todo_owner = TodoOwner(owner_id="123")
        categories = [Category(name="test"), Category(name="again")]
        tags = [Tag(name="who"), Tag(name="knows")]
        actions = [Action()]
        task = Task(todo_id="abc",
                    todo_owner=todo_owner,
                    name="reoccur",
                    description="description",
                    completion_points=1,
                    due_date=datetime.datetime(2019, 3, 3, 0, 25, 5),
                    categories=categories,
                    tags=tags,
                    actions=actions)
        return task

    @freeze_time("2019-02-24")
    def test_get_todo_task(self, user_request, todo_repo):
        task = self._create_task()
        todo_repo.add(task)

        todo = GetTodo().execute(todo_id="abc")

        assert todo is not None
        assert todo.todo_id == "abc"

    def test_get_todo_unauthorized(self, user_request, todo_repo):
        task = self._create_task()
        task.todo_owner.owner_id = "456"
        todo_repo.add(task)

        with pytest.raises(UnauthorizedError):
            GetTodo().execute(todo_id="abc")

    def test_get_todo_not_found(self, todo_repo):
        with pytest.raises(NotFoundError):
            GetTodo().execute(todo_id="def")

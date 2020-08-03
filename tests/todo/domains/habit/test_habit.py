import datetime

from freezegun import freeze_time

from app.todo.domains.action import Action
from app.todo.domains.category import Category
from app.todo.domains.habit.habit import Habit
from app.todo.domains.habit.habit_buffer import HabitBufferType, HabitBuffer
from app.todo.domains.habit.habit_period import HabitPeriod, HabitPeriodType
from app.todo.domains.tag import Tag
from app.todo.domains.todo_owner import TodoOwner


@freeze_time("2019-02-24 10:00:04")
def test_to_dict():
    todo_owner = TodoOwner(owner_id="123")
    period = HabitPeriod(period_type=HabitPeriodType.WEEKS,
                         amount=1)
    buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                         amount=1)
    tags = [Tag(name="who"), Tag(name="knows")]
    actions = [Action(action_id="fgh", points=2)]
    habit = Habit(todo_id="abc",
                  todo_owner=todo_owner,
                  name="habit",
                  description="description",
                  points_per=1,
                  completion_points=1,
                  frequency=1,
                  period=period,
                  buffer=buffer,
                  category=Category(category_id="abc",
                                    name="test",
                                    color="#FFF"),
                  tags=tags,
                  actions=actions)

    assert habit.to_dict() == {
        "todoId": "abc",
        "todoOwnerId": "123",
        "name": "habit",
        "description": "description",
        "todoType": "HABIT",
        "pointsPer": 1,
        "completionPoints": 1,
        "frequency": 1,
        "period": {
            "periodType": "WEEKS",
            "amount": 1
        },
        "buffer": {
            "bufferType": "DAY_START",
            "amount": 1,
        },
        "category": {
            "id": "abc",
            "name": "test",
            "color": "#FFF"
        },
        "tags": ["who", "knows"],
        "createdDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
        "modifiedDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
        "actions": [{
            "actionId": "fgh",
            "actionDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
            "points": 2
        }],
        "actionsWithinPeriod": [],
        "shouldShow": False
    }


class TestIsCompleteDays:
    @freeze_time("2019-03-03 21:00:00")
    def test_is_complete_one_per_day_new(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS,
                             amount=1)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period)

        assert habit.is_complete is False

    @freeze_time("2019-03-03 21:00:00")
    def test_is_complete_one_per_day_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS,
                             amount=1)
        actions = [Action(action_date=datetime.datetime(2019, 3, 3, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      actions=actions)

        assert habit.is_complete is True

    @freeze_time("2019-03-03 21:00:00")
    def test_is_complete_one_per_day_incomplete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS,
                             amount=1)
        # did it yesterday
        actions = [Action(action_date=datetime.datetime(2019, 3, 2, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      actions=actions)

        assert habit.is_complete is False

    @freeze_time("2019-03-03 21:00:00")
    def test_is_complete_twice_per_day_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS,
                             amount=1)
        actions = [Action(action_date=datetime.datetime(2019, 3, 3, 11, 0, 0),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 3, 3, 16, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      actions=actions)

        assert habit.is_complete is True

    @freeze_time("2019-03-03 21:00:00")
    def test_is_complete_twice_per_day_incomplete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS,
                             amount=1)
        actions = [Action(action_date=datetime.datetime(2019, 3, 3, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      actions=actions)

        assert habit.is_complete is False


class TestIsCompleteWeeks:
    @freeze_time("2019-03-07 21:00:00")
    def test_is_complete_one_per_week_new(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period)

        assert habit.is_complete is False

    @freeze_time("2019-03-07 21:00:00")
    def test_is_complete_one_per_week_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        actions = [Action(action_date=datetime.datetime(2019, 3, 5, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      actions=actions)

        assert habit.is_complete is True

    @freeze_time("2019-03-07 21:00:00")
    def test_is_complete_one_per_week_incomplete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)

        # did it last week, not this week
        actions = [Action(action_date=datetime.datetime(2019, 3, 3, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      actions=actions)

        assert habit.is_complete is False

    @freeze_time("2019-03-07 21:00:00")
    def test_is_complete_twice_per_week_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 0, 0),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 3, 6, 16, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      actions=actions)

        assert habit.is_complete is True

    @freeze_time("2019-03-07 21:00:00")
    def test_is_complete_twice_per_week_incomplete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        actions = [Action(action_date=datetime.datetime(2019, 3, 5, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      actions=actions)

        assert habit.is_complete is False


class TestIsCompleteMonths:
    @freeze_time("2019-03-22 21:00:00")
    def test_is_complete_one_per_month_new(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period)

        assert habit.is_complete is False

    @freeze_time("2019-03-22 21:00:00")
    def test_is_complete_one_per_month_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        actions = [Action(action_date=datetime.datetime(2019, 3, 5, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      actions=actions)

        assert habit.is_complete is True

    @freeze_time("2019-03-22 21:00:00")
    def test_is_complete_one_per_month_incomplete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)

        # did it last month, not this month
        actions = [Action(action_date=datetime.datetime(2019, 2, 28, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      actions=actions)

        assert habit.is_complete is False

    @freeze_time("2019-03-22 21:00:00")
    def test_is_complete_twice_per_months_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 0, 0),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 3, 12, 16, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      actions=actions)

        assert habit.is_complete is True

    @freeze_time("2019-03-22 21:00:00")
    def test_is_complete_twice_per_month_incomplete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        actions = [Action(action_date=datetime.datetime(2019, 3, 14, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      actions=actions)

        assert habit.is_complete is False


class TestIsCompleteYears:
    @freeze_time("2019-07-22 21:00:00")
    def test_is_complete_one_per_year_new(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period)

        assert habit.is_complete is False

    @freeze_time("2019-07-22 21:00:00")
    def test_is_complete_one_per_year_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        actions = [Action(action_date=datetime.datetime(2019, 3, 5, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      actions=actions)

        assert habit.is_complete is True

    @freeze_time("2019-07-22 21:00:00")
    def test_is_complete_one_per_year_incomplete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)

        # did it last year, not this year
        actions = [Action(action_date=datetime.datetime(2018, 8, 28, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      actions=actions)

        assert habit.is_complete is False

    @freeze_time("2019-07-22 21:00:00")
    def test_is_complete_twice_per_year_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        actions = [Action(action_date=datetime.datetime(2019, 1, 4, 11, 0, 0),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 6, 12, 16, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      actions=actions)

        assert habit.is_complete is True

    @freeze_time("2019-07-22 21:00:00")
    def test_is_complete_twice_per_year_incomplete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        actions = [Action(action_date=datetime.datetime(2019, 3, 14, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      actions=actions)

        assert habit.is_complete is False


class TestShouldShowHours:
    @freeze_time("2019-03-05 21:00:00")
    def test_should_show_no_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period)

        assert habit.should_show is True

    @freeze_time("2019-03-05 21:00:00")
    def test_should_show_no_actions(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.HOURS,
                             amount=4)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      buffer=buffer)

        assert habit.should_show is True

    @freeze_time("2019-03-05 21:00:00")
    def test_should_show_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.HOURS,
                             amount=4)
        actions = [Action(action_date=datetime.datetime(2019, 3, 5, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=1,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-05 21:00:00")
    def test_should_show_within_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.HOURS,
                             amount=4)
        # 2 hours ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 5, 19, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-05 21:00:00")
    def test_should_show_outside_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.DAYS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.HOURS,
                             amount=4)

        # 6 hours ago, outside buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 5, 15, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is True


class TestShouldShowDayStarts:
    @freeze_time("2019-03-08 4:30:00")
    def test_should_show_no_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period)

        assert habit.should_show is True

    @freeze_time("2019-03-08 4:30:00")
    def test_should_show_no_actions(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=2)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer)

        assert habit.should_show is True

    @freeze_time("2019-03-08 4:30:00")
    def test_should_show_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=2)
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 0, 0),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 3, 5, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-08 00:30:00")
    def test_should_show_within_buffer_right_after_midnight(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=1)
        # 1 day ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 7, 19, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-08 00:30:00")
    def test_should_show_within_buffer_right_after_midnight_action_after_midnight(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=1)
        # 1 day ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 8, 0, 0, 11),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-08 04:30:00")
    def test_should_show_outside_buffer_early_morning(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=1)
        # 1 day ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 7, 19, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is True

    @freeze_time("2019-03-08 04:30:00")
    def test_should_show_outside_buffer_early_morning_action_after_midnight(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=1)
        # 1 day ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 8, 0, 0, 11),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is True

    @freeze_time("2019-03-08 4:30:00")
    def test_should_show_within_buffer_early_morning_mutlti_day(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=2)
        # 1 day ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 7, 19, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-08 4:30:00")
    def test_should_show_outside_buffer_early_morning_mutlti_day(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAY_START,
                             amount=2)

        # 2 days ago at 9pm which is less than 2 days but is 2 day starts, outside buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 6, 21, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is True


class TestShouldShowDays:
    @freeze_time("2019-03-08 21:00:00")
    def test_should_show_no_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period)

        assert habit.should_show is True

    @freeze_time("2019-03-08 21:00:00")
    def test_should_show_no_actions(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAYS,
                             amount=2)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer)

        assert habit.should_show is True

    @freeze_time("2019-03-08 21:00:00")
    def test_should_show_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAYS,
                             amount=2)
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 0, 0),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 3, 5, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-08 21:00:00")
    def test_should_show_within_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAYS,
                             amount=2)
        # 1 day ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 7, 19, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-08 21:00:00")
    def test_should_show_outside_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.WEEKS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.DAYS,
                             amount=2)

        # 4 days ago, outside buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 15, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is True


class TestShouldShowWeeks:
    @freeze_time("2019-03-28 21:00:00")
    def test_should_show_no_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period)

        assert habit.should_show is True

    @freeze_time("2019-03-28 21:00:00")
    def test_should_show_no_actions(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.WEEKS,
                             amount=2)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer)

        assert habit.should_show is True

    @freeze_time("2019-03-28 21:00:00")
    def test_should_show_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.WEEKS,
                             amount=2)
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 0, 0),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 3, 12, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-28 21:00:00")
    def test_should_show_within_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.WEEKS,
                             amount=2)
        # 1 week ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 20, 19, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-03-28 21:00:00")
    def test_should_show_outside_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.MONTHS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.WEEKS,
                             amount=2)

        # 3 weeks ago, outside buffer
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 15, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is True


class TestShouldShowMonths:
    @freeze_time("2019-11-28 21:00:00")
    def test_should_show_no_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period)

        assert habit.should_show is True

    @freeze_time("2019-11-28 21:00:00")
    def test_should_show_no_actions(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.MONTHS,
                             amount=2)
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer)

        assert habit.should_show is True

    @freeze_time("2019-11-28 21:00:00")
    def test_should_show_complete(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.MONTHS,
                             amount=2)
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 0, 0),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 6, 12, 11, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-11-28 21:00:00")
    def test_should_show_within_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.MONTHS,
                             amount=2)
        # 1 month ago, within buffer
        actions = [Action(action_date=datetime.datetime(2019, 10, 20, 19, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is False

    @freeze_time("2019-11-28 21:00:00")
    def test_should_show_outside_buffer(self):
        todo_owner = TodoOwner(owner_id="123")
        period = HabitPeriod(period_type=HabitPeriodType.YEARS)
        buffer = HabitBuffer(buffer_type=HabitBufferType.MONTHS,
                             amount=2)

        # 3 months ago, outside buffer
        actions = [Action(action_date=datetime.datetime(2019, 8, 4, 15, 0, 0),
                          points=1)]
        habit = Habit(todo_id="abc",
                      todo_owner=todo_owner,
                      name="habit",
                      description="description",
                      points_per=1,
                      completion_points=1,
                      frequency=2,
                      period=period,
                      buffer=buffer,
                      actions=actions)

        assert habit.should_show is True

import datetime

from freezegun import freeze_time

from app.todo.domains.action import Action
from app.todo.domains.category import Category
from app.todo.domains.reoccur.reoccur import Reoccur
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.tag import Tag
from app.todo.domains.todo_owner import TodoOwner


@freeze_time("2019-02-24 10:00:04")
def test_to_dict():
    todo_owner = TodoOwner(owner_id="123")
    repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                           when=["Sunday"])
    categories = [Category(name="test"), Category(name="again")]
    tags = [Tag(name="who"), Tag(name="knows")]
    actions = [Action(points=2)]
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

    assert reoccur.to_dict() == {
        "todoId": "abc",
        "todoOwnerId": "123",
        "name": "reoccur",
        "description": "description",
        "todoType": "REOCCUR",
        "completionPoints": 1,
        "required": False,
        "repeat": {
            "repeatType": "DAY_OF_WEEK",
            "when": ["Sunday"],
        },
        "categories": ["test", "again"],
        "tags": ["who", "knows"],
        "createdDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
        "modifiedDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
        "actions": [{
            "actionDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
            "points": 2
        }]
    }


class TestShouldShowDayOfWeek:
    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_no_action_on_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Thursday is 3/7
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Thursday"])
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=False,
                          repeat=repeat)

        assert reoccur.should_show is True

    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_no_action_not_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday"])
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=False,
                          repeat=repeat)

        assert reoccur.should_show is False

    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_complete_today(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4 Thursday is 3/7
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday", "Thursday"])
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 12, 5),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 3, 7, 11, 12, 5),
                          points=1)
                   ]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=False,
                          repeat=repeat,
                          actions=actions)

        assert reoccur.should_show is False

    @freeze_time("2019-03-07 21:00:00")
    def test_is_should_show_of_week_complete_not_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4 Friday is 3/8
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday", "Friday"])
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 12, 5),
                          points=1)]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=False,
                          repeat=repeat,
                          actions=actions)

        assert reoccur.should_show is False

    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_complete_not_complete_on_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4 Thursday is 3/7
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday", "Thursday"])
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 12, 5),
                          points=1)]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=False,
                          repeat=repeat,
                          actions=actions)

        assert reoccur.should_show is True


class TestShouldShowDayOfWeekRequired:
    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_no_action_on_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Thursday is 3/7
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Thursday"])
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=True,
                          repeat=repeat)

        assert reoccur.should_show is True

    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_no_action_not_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday"])
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=True,
                          repeat=repeat)

        assert reoccur.should_show is True

    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_complete_today(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4 Thursday is 3/7
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday", "Thursday"])
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 12, 5),
                          points=1),
                   Action(action_date=datetime.datetime(2019, 3, 7, 11, 12, 5),
                          points=1)
                   ]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=True,
                          repeat=repeat,
                          actions=actions)

        assert reoccur.should_show is False

    @freeze_time("2019-03-07 21:00:00")
    def test_is_should_show_of_week_complete_not_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4 Friday is 3/8
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday", "Friday"])
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 12, 5),
                          points=1)]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=True,
                          repeat=repeat,
                          actions=actions)

        assert reoccur.should_show is False

    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_complete_not_complete_on_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4 Thursday is 3/7
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday", "Thursday"])
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 12, 5),
                          points=1)]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=True,
                          repeat=repeat,
                          actions=actions)

        assert reoccur.should_show is True

    @freeze_time("2019-03-07 21:00:00")
    def test_should_show_day_of_week_not_complete_not_on_repeat_day(self):
        todo_owner = TodoOwner(owner_id="123")
        # Monday is 3/4 Thursday is 3/6
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                               when=["Monday", "Wednesday"])
        actions = [Action(action_date=datetime.datetime(2019, 3, 4, 11, 12, 5),
                          points=1)]
        reoccur = Reoccur(todo_id="abc",
                          todo_owner=todo_owner,
                          name="reoccur",
                          description="description",
                          completion_points=1,
                          required=True,
                          repeat=repeat,
                          actions=actions)

        assert reoccur.should_show is True

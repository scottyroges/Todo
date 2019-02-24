import datetime

from freezegun import freeze_time

from app.todo.domains.action import Action


def test_to_dict():
    action = Action(
        action_id="abc",
        action_date=datetime.datetime(2019, 2, 24),
        points=4
    )

    assert action.to_dict() == {
        "actionDate": datetime.datetime(2019, 2, 24),
        "points": 4
    }


@freeze_time("2019-02-24 10:00:04")
def test_default_date():
    action = Action(
        points=4
    )

    assert action.action_date == datetime.datetime(2019, 2, 24, 10, 0, 4)
    assert action.points == 4

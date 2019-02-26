import datetime
import json

import pytest

from app.model import (
    Habit as HabitRecord,
    Category as CategoryRecord,
    Tag as TagRecord,
    Action as ActionRecord
)
from app.todo.domains.todo_type import TodoType


@pytest.mark.integration
def test_habit_create(client, session, mocker):
    todo_data = {
        "name": "habit_test",
        "todoOwnerId": "123",
        "description": "description",
        "pointsPer": 1,
        "completionPoints": 1,
        "frequency": 1,
        "buffer": {
            "bufferType": "DAY_START",
            "amount": 1
        },
        "period": {
            "periodType": "WEEKS",
            "amount": 1
        },
        "categories": ["test", "again"],
        "tags": ["who", "knows"]
    }
    data = json.dumps(todo_data)
    mocker.patch("app.auth.auth_decorator.authorize_request",
                 return_value={"sub": "123"})
    create_resp = client.post('/habit',
                              data=data,
                              headers={'Authorization': 'fake_token'})
    create_data = json.loads(create_resp.data.decode('utf-8'))
    assert create_data is not None
    assert create_data["todoId"] is not None

    habit_record = session.query(HabitRecord).get(create_data.get("todoId"))

    assert habit_record is not None
    assert habit_record.todo_id is not None
    assert habit_record.todo_owner_id == todo_data["todoOwnerId"]
    assert habit_record.name == todo_data["name"]
    assert habit_record.description == todo_data["description"]
    assert habit_record.todo_type == TodoType.HABIT
    assert habit_record.points_per == todo_data["pointsPer"]
    assert habit_record.completion_points == todo_data["completionPoints"]
    assert habit_record.period == {'amount': 1, 'periodType': 'WEEKS', 'start': None}
    assert habit_record.buffer == {'amount': 1, 'bufferType': 'DAY_START'}
    # assert sorted(habit_record.categories) == sorted(todo_data["categories"])
    # assert sorted(habit_record.tags) == sorted(todo_data["tags"])
    # assert todo_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
    # assert todo_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
    # assert todo_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"


@pytest.mark.integration
def test_habit_create_unauthorized():
    pass


@pytest.mark.integration
def test_habit_create_admin():
    pass


@pytest.mark.integration
def test_habit_read(client, session, mocker):
    period = {
        'amount': 1,
        'periodType': 'WEEKS',
        'start': None
    }
    buffer = {
        'amount': 1,
        'bufferType': 'DAY_START'
    }
    categories = [CategoryRecord(name="test"), CategoryRecord(name="again")]
    tags = [TagRecord(name="who"), TagRecord(name="knows")]
    actions = [ActionRecord(action_date=datetime.datetime(2019, 2, 24),
                            points=1)]
    habit_record = HabitRecord(todo_id="abc",
                               todo_owner_id="123",
                               name="habit",
                               description="description",
                               todo_type=TodoType.HABIT,
                               points_per=1,
                               completion_points=1,
                               frequency=1,
                               period=period,
                               buffer=buffer,
                               categories=categories,
                               tags=tags,
                               actions=actions,
                               created_date=datetime.datetime(2019, 2, 24),
                               modified_date=datetime.datetime(2019, 2, 24))
    session.add(habit_record)
    session.commit()

    mocker.patch("app.auth.auth_decorator.authorize_request",
                 return_value={"sub": "123"})
    fetch_resp = client.get('/habit/%s' % habit_record.todo_id,
                            headers={'Authorization': 'fake_token'})
    fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

    assert fetch_data is not None
    assert fetch_data["todoId"] == habit_record.todo_id
    assert fetch_data["todoOwnerId"] == habit_record.todo_owner_id
    assert fetch_data["name"] == habit_record.name
    assert fetch_data["description"] == habit_record.description
    assert fetch_data["todoType"] == habit_record.todo_type.name
    assert fetch_data["pointsPer"] == habit_record.points_per
    assert fetch_data["completionPoints"] == habit_record.completion_points
    assert fetch_data["period"] == {'amount': 1, 'periodType': 'WEEKS', 'start': None}
    assert fetch_data["buffer"] == {'amount': 1, 'bufferType': 'DAY_START'}
    assert sorted(fetch_data["categories"]) == sorted(["test", "again"])
    assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
    assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
    assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
    assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"


@pytest.mark.integration
def test_habit_read_unauthorized():
    pass


@pytest.mark.integration
def test_habit_read_admin():
    pass


@pytest.mark.integration
def test_habit_read_not_found(client, session, mocker):
    mocker.patch("app.auth.auth_decorator.authorize_request",
                 return_value={"sub": "123"})
    fetch_resp = client.get('/habit/%s' % "abc",
                            headers={'Authorization': 'fake_token'})

    assert fetch_resp.status_code == 404

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
def test_action_create(client, session, mocker):
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
                               created_date=datetime.datetime(2019, 2, 24),
                               modified_date=datetime.datetime(2019, 2, 24))
    session.add(habit_record)
    session.commit()

    action_data = {
        "actionDate": "2019-02-21 12:02:05",
        "points": "1",
        "todoId": habit_record.todo_id
    }
    data = json.dumps(action_data)
    mocker.patch("app.auth.auth_decorator.authorize_request",
                 return_value={"sub": "123"})
    create_resp = client.post('/action',
                              data=data,
                              headers={'Authorization': 'fake_token'})
    create_data = json.loads(create_resp.data.decode('utf-8'))

    assert create_data is not None
    print(create_data)
    action_record = session.query(ActionRecord).filter(ActionRecord.todo_id == habit_record.todo_id)

    assert action_record is not None


@pytest.mark.integration
def test_action_create_unauthorized():
    pass


@pytest.mark.integration
def test_action_create_admin():
    pass

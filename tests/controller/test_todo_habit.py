import json
import pytest

from app.model import (
    Habit as HabitRecord,

)
from app.todo.domains.todo_type import TodoType
from app.utils import make


@pytest.mark.integration
def test_habit_create(client, session, test_user):
    category = make.a_category(session)
    todo_data = {
        "name": "habit_test",
        "description": "description",
        "pointsPer": 1,
        "completionPoints": 1,
        "frequency": 1,
        "todoType": "HABIT",
        "buffer": {
            "bufferType": "DAY_START",
            "amount": 1
        },
        "period": {
            "periodType": "WEEKS",
            "amount": 1
        },
        "category": {
            "id": category.id
        },
        "tags": ["who", "knows"]
    }

    make.a_category(session)

    data = json.dumps(todo_data)
    create_resp = client.post('/todo',
                              data=data,
                              headers={'Authorization': test_user.get("token")})
    assert create_resp.status_code == 200

    create_data = json.loads(create_resp.data.decode('utf-8'))
    assert create_data is not None
    assert create_data["todoId"] is not None
    assert create_data["todoOwnerId"] == test_user.get("user_id")
    assert create_data["name"] == todo_data["name"]
    assert create_data["description"] == todo_data["description"]
    assert create_data["todoType"] == "HABIT"
    assert create_data["pointsPer"] == todo_data["pointsPer"]
    assert create_data["completionPoints"] == todo_data["completionPoints"]
    assert create_data["frequency"] == todo_data["frequency"]
    assert create_data["period"] == {'amount': 1, 'periodType': 'WEEKS'}
    assert create_data["buffer"] == {'amount': 1, 'bufferType': 'DAY_START'}
    assert create_data["category"] == {'id': category.id, "name": "test", "color": "#FFF"}
    assert sorted(create_data["tags"]) == sorted(["who", "knows"])
    assert create_data["actions"] == []
    assert create_data["createdDate"] is not None
    assert create_data["modifiedDate"] is not None

    habit_record = session.query(HabitRecord).get(create_data.get("todoId"))

    assert habit_record is not None
    assert habit_record.todo_id is not None
    assert habit_record.todo_owner_id == test_user.get("user_id")
    assert habit_record.name == todo_data["name"]
    assert habit_record.description == todo_data["description"]
    assert habit_record.todo_type == TodoType.HABIT
    assert habit_record.points_per == todo_data["pointsPer"]
    assert habit_record.completion_points == todo_data["completionPoints"]
    assert habit_record.frequency == todo_data["frequency"]
    assert habit_record.period == {'amount': 1, 'periodType': 'WEEKS'}
    assert habit_record.buffer == {'amount': 1, 'bufferType': 'DAY_START'}
    assert habit_record.category.id == category.id
    assert habit_record.category.name == "test"
    assert habit_record.category.color == "#FFF"
    assert len(habit_record.tags) == 2
    for tag in habit_record.tags:
        assert tag.name in ["who", "knows"]
    assert len(habit_record.actions) == 0
    assert habit_record.created_date is not None
    assert habit_record.modified_date is not None


@pytest.mark.integration
def test_habit_create_unauthorized(client, session, test_user):
    todo_data = {
        "name": "habit_test",
        "todoOwnerId": "123",
        "description": "description",
        "todoType": "HABIT",
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
        "category": {
            "id": "abc",
            "name": "test",
            "color": "#FFF"
        },
        "tags": ["who", "knows"]
    }
    data = json.dumps(todo_data)
    create_resp = client.post('/todo',
                              data=data,
                              headers={'Authorization': test_user.get("token")})
    assert create_resp.status_code == 401


@pytest.mark.integration
def test_habit_create_admin(client, session, test_admin):
    category = make.a_category(session)

    todo_data = {
        "name": "habit_test",
        "todoOwnerId": "123",
        "description": "description",
        "todoType": "HABIT",
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
        "category": {
            "id": category.id
        },
        "tags": ["who", "knows"]
    }



    data = json.dumps(todo_data)
    create_resp = client.post('/todo',
                              data=data,
                              headers={'Authorization': test_admin.get("token")})
    assert create_resp.status_code == 200

    create_data = json.loads(create_resp.data.decode('utf-8'))
    assert create_data is not None
    assert create_data["todoId"] is not None
    assert create_data["todoOwnerId"] == todo_data["todoOwnerId"]
    assert create_data["name"] == todo_data["name"]
    assert create_data["description"] == todo_data["description"]
    assert create_data["todoType"] == "HABIT"
    assert create_data["pointsPer"] == todo_data["pointsPer"]
    assert create_data["frequency"] == todo_data["frequency"]
    assert create_data["completionPoints"] == todo_data["completionPoints"]
    assert create_data["period"] == {'amount': 1, 'periodType': 'WEEKS'}
    assert create_data["buffer"] == {'amount': 1, 'bufferType': 'DAY_START'}
    assert create_data["category"] == {'id': category.id, "name": "test", "color": "#FFF"}
    assert sorted(create_data["tags"]) == sorted(["who", "knows"])
    assert create_data["actions"] == []
    assert create_data["createdDate"] is not None
    assert create_data["modifiedDate"] is not None

    habit_record = session.query(HabitRecord).get(create_data.get("todoId"))

    assert habit_record is not None
    assert habit_record.todo_id is not None
    assert habit_record.todo_owner_id == "123"
    assert habit_record.name == todo_data["name"]
    assert habit_record.description == todo_data["description"]
    assert habit_record.todo_type == TodoType.HABIT
    assert habit_record.points_per == todo_data["pointsPer"]
    assert habit_record.completion_points == todo_data["completionPoints"]
    assert habit_record.frequency == todo_data["frequency"]
    assert habit_record.period == {'amount': 1, 'periodType': 'WEEKS'}
    assert habit_record.buffer == {'amount': 1, 'bufferType': 'DAY_START'}
    assert habit_record.category.id == category.id
    assert habit_record.category.name == "test"
    assert habit_record.category.color == "#FFF"
    assert len(habit_record.tags) == 2
    for tag in habit_record.tags:
        assert tag.name in ["who", "knows"]
    assert len(habit_record.actions) == 0
    assert habit_record.created_date is not None
    assert habit_record.modified_date is not None


@pytest.mark.integration
def test_habit_read(client, session, test_user):
    habit_record = make.a_habit(
        session,
        todo_owner_id=test_user.get("user_id"),
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")],
        actions=[make.an_action(session)]
    )

    fetch_resp = client.get('/todo/%s' % habit_record.todo_id,
                            headers={'Authorization': test_user.get("token")})
    assert fetch_resp.status_code == 200

    fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

    assert fetch_data is not None
    assert fetch_data["todoId"] == habit_record.todo_id
    assert fetch_data["todoOwnerId"] == habit_record.todo_owner_id
    assert fetch_data["name"] == habit_record.name
    assert fetch_data["description"] == habit_record.description
    assert fetch_data["todoType"] == habit_record.todo_type.name
    assert fetch_data["pointsPer"] == habit_record.points_per
    assert fetch_data["completionPoints"] == habit_record.completion_points
    assert fetch_data["frequency"] == habit_record.frequency
    assert fetch_data["period"] == {'amount': 1, 'periodType': 'WEEKS'}
    assert fetch_data["buffer"] == {'amount': 1, 'bufferType': 'DAY_START'}
    assert fetch_data["category"] == {'id': habit_record.category_id, "name": "test", "color": "#FFF"}
    assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
    assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
    assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
    assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"


@pytest.mark.integration
def test_habit_read_unauthorized(client, session, test_user):
    habit_record = make.a_habit(
        session,
        todo_owner_id="123",
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")],
        actions=[make.an_action(session)]
    )
    session.add(habit_record)
    session.commit()

    fetch_resp = client.get('/todo/%s' % habit_record.todo_id,
                            headers={'Authorization': test_user.get("token")})
    assert fetch_resp.status_code == 401


@pytest.mark.integration
def test_habit_read_admin(client, session, test_admin):
    habit_record = make.a_habit(
        session,
        todo_owner_id="123",
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")],
        actions=[make.an_action(session)]
    )
    session.add(habit_record)
    session.commit()

    fetch_resp = client.get('/todo/%s' % habit_record.todo_id,
                            headers={'Authorization': test_admin.get("token")})
    assert fetch_resp.status_code == 200

    fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

    assert fetch_data is not None
    assert fetch_data["todoId"] == habit_record.todo_id
    assert fetch_data["todoOwnerId"] == habit_record.todo_owner_id
    assert fetch_data["name"] == habit_record.name
    assert fetch_data["description"] == habit_record.description
    assert fetch_data["todoType"] == habit_record.todo_type.name
    assert fetch_data["pointsPer"] == habit_record.points_per
    assert fetch_data["completionPoints"] == habit_record.completion_points
    assert fetch_data["frequency"] == habit_record.frequency
    assert fetch_data["period"] == {'amount': 1, 'periodType': 'WEEKS'}
    assert fetch_data["buffer"] == {'amount': 1, 'bufferType': 'DAY_START'}
    assert fetch_data["category"] == {'id': habit_record.category_id, "name": "test", "color": "#FFF"}
    assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
    assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
    assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
    assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"


@pytest.mark.integration
def test_habit_read_not_found(client, session, test_user):
    fetch_resp = client.get('/todo/%s' % "abc",
                            headers={'Authorization': test_user.get("token")})

    assert fetch_resp.status_code == 404

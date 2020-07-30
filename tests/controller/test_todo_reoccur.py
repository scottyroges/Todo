import json

import pytest
from app.model import (
    Reoccur as ReoccurRecord,
)
from app.todo.domains.todo_type import TodoType
from app.utils import make


@pytest.mark.integration
def test_reoccur_create(client, session, test_user):
    category = make.a_category(session)
    todo_data = {
        "name": "reoccur_test",
        "description": "description",
        "todoType": "REOCCUR",
        "completionPoints": 1,
        "repeat": {
            "repeatType": "DAY_OF_WEEK",
            "when": ["Sunday"]
        },
        "category": {
            "id": category.id
        },
        "tags": ["who", "knows"],
        "required": False
    }

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
    assert create_data["todoType"] == "REOCCUR"
    assert create_data["completionPoints"] == todo_data["completionPoints"]
    assert create_data["repeat"] == {'when': ["Sunday"], 'repeatType': 'DAY_OF_WEEK'}
    assert create_data["required"] is False
    assert create_data["category"] == {'id': category.id, "name": "test", "color": "#FFF"}
    assert sorted(create_data["tags"]) == sorted(["who", "knows"])
    assert create_data["actions"] == []
    assert create_data["createdDate"] is not None
    assert create_data["modifiedDate"] is not None

    reoccur_record = session.query(ReoccurRecord).get(create_data.get("todoId"))

    assert reoccur_record is not None
    assert reoccur_record.todo_id is not None
    assert reoccur_record.todo_owner_id == test_user.get("user_id")
    assert reoccur_record.name == todo_data["name"]
    assert reoccur_record.description == todo_data["description"]
    assert reoccur_record.todo_type == TodoType.REOCCUR
    assert reoccur_record.completion_points == todo_data["completionPoints"]
    assert reoccur_record.repeat == {'when': ["Sunday"], 'repeatType': 'DAY_OF_WEEK'}
    assert reoccur_record.required == todo_data['required']
    assert reoccur_record.category.id == category.id
    assert reoccur_record.category.name == "test"
    assert reoccur_record.category.color == "#FFF"
    assert len(reoccur_record.tags) == 2
    for tag in reoccur_record.tags:
        assert tag.name in ["who", "knows"]
    assert len(reoccur_record.actions) == 0
    assert reoccur_record.created_date is not None
    assert reoccur_record.modified_date is not None


@pytest.mark.integration
def test_reoccur_create_unauthorized(client, session, test_user):
    category = make.a_category(session)
    todo_data = {
        "name": "reoccur_test",
        "todoOwnerId": "123",
        "description": "description",
        "todoType": "REOCCUR",
        "completionPoints": 1,
        "repeat": {
            "repeatType": "DAY_OF_WEEK",
            "when": ["Sunday"]
        },
        "category": {
            "id": category.id
        },
        "tags": ["who", "knows"],
        "required": False
    }
    data = json.dumps(todo_data)
    create_resp = client.post('/todo',
                              data=data,
                              headers={'Authorization': test_user.get("token")})
    assert create_resp.status_code == 401


@pytest.mark.integration
def test_reoccur_create_admin(client, session, test_admin):
    category = make.a_category(session)
    todo_data = {
        "name": "reoccur_test",
        "todoOwnerId": "123",
        "description": "description",
        "todoType": "REOCCUR",
        "completionPoints": 1,
        "repeat": {
            "repeatType": "DAY_OF_WEEK",
            "when": ["Sunday"]
        },
        "category": {
            "id": category.id
        },
        "tags": ["who", "knows"],
        "required": False
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
    assert create_data["todoType"] == "REOCCUR"
    assert create_data["completionPoints"] == todo_data["completionPoints"]
    assert create_data["repeat"] == {'when': ["Sunday"], 'repeatType': 'DAY_OF_WEEK'}
    assert create_data["required"] is False
    assert create_data["category"] == {'id': category.id, "name": "test", "color": "#FFF"}
    assert sorted(create_data["tags"]) == sorted(["who", "knows"])
    assert create_data["actions"] == []
    assert create_data["createdDate"] is not None
    assert create_data["modifiedDate"] is not None

    reoccur_record = session.query(ReoccurRecord).get(create_data.get("todoId"))

    assert reoccur_record is not None
    assert reoccur_record.todo_id is not None
    assert reoccur_record.todo_owner_id == todo_data["todoOwnerId"]
    assert reoccur_record.name == todo_data["name"]
    assert reoccur_record.description == todo_data["description"]
    assert reoccur_record.todo_type == TodoType.REOCCUR
    assert reoccur_record.completion_points == todo_data["completionPoints"]
    assert reoccur_record.repeat == {'when': ["Sunday"], 'repeatType': 'DAY_OF_WEEK'}
    assert reoccur_record.required == todo_data['required']
    assert reoccur_record.category.id == category.id
    assert reoccur_record.category.name == "test"
    assert reoccur_record.category.color == "#FFF"
    assert len(reoccur_record.tags) == 2
    for tag in reoccur_record.tags:
        assert tag.name in ["who", "knows"]
    assert len(reoccur_record.actions) == 0
    assert reoccur_record.created_date is not None
    assert reoccur_record.modified_date is not None


@pytest.mark.integration
def test_reoccur_read(client, session, test_user):
    reoccur_record = make.a_reoccur(
        session,
        todo_owner_id=test_user.get("user_id"),
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")],
        actions=[make.an_action(session)]
    )

    fetch_resp = client.get('/todo/%s' % reoccur_record.todo_id,
                            headers={'Authorization': test_user.get("token")})
    assert fetch_resp.status_code == 200

    fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

    assert fetch_data is not None
    assert fetch_data["todoId"] == reoccur_record.todo_id
    assert fetch_data["todoOwnerId"] == reoccur_record.todo_owner_id
    assert fetch_data["name"] == reoccur_record.name
    assert fetch_data["description"] == reoccur_record.description
    assert fetch_data["todoType"] == reoccur_record.todo_type.name
    assert fetch_data["completionPoints"] == reoccur_record.completion_points
    assert fetch_data["required"] == reoccur_record.required
    assert fetch_data["repeat"] == {'when': ["Sunday"], 'repeatType': 'DAY_OF_WEEK'}
    assert fetch_data["category"] == {'id': reoccur_record.category_id, "name": "test", "color": "#FFF"}
    assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
    assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', 'points': 1}]
    assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
    assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"


@pytest.mark.integration
def test_reoccur_read_unauthorized(client, session, test_user):
    reoccur_record = make.a_reoccur(
        session,
        todo_owner_id="123",
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")]
    )

    fetch_resp = client.get('/todo/%s' % reoccur_record.todo_id,
                            headers={'Authorization': test_user.get("token")})
    assert fetch_resp.status_code == 401


@pytest.mark.integration
def test_reoccur_read_admin(client, session, test_admin):
    reoccur_record = make.a_reoccur(
        session,
        todo_owner_id="123",
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")],
        actions=[make.an_action(session)]
    )

    fetch_resp = client.get('/todo/%s' % reoccur_record.todo_id,
                            headers={'Authorization': test_admin.get("token")})
    assert fetch_resp.status_code == 200

    fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

    assert fetch_data is not None
    assert fetch_data["todoId"] == reoccur_record.todo_id
    assert fetch_data["todoOwnerId"] == reoccur_record.todo_owner_id
    assert fetch_data["name"] == reoccur_record.name
    assert fetch_data["description"] == reoccur_record.description
    assert fetch_data["todoType"] == reoccur_record.todo_type.name
    assert fetch_data["completionPoints"] == reoccur_record.completion_points
    assert fetch_data["required"] == reoccur_record.required
    assert fetch_data["repeat"] == {'when': ["Sunday"], 'repeatType': 'DAY_OF_WEEK'}
    assert fetch_data["category"] == {'id': reoccur_record.category_id, "name": "test", "color": "#FFF"}
    assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
    assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
    assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
    assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"


@pytest.mark.integration
def test_reoccur_read_not_found(client, session, test_user):
    fetch_resp = client.get('/todo/%s' % "abc",
                            headers={'Authorization': test_user.get("token")})

    assert fetch_resp.status_code == 404

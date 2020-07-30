import datetime
import json
import pytest

from app.model import (
    Task as TaskRecord
)
from app.todo.domains.todo_type import TodoType
from app.utils import make


@pytest.mark.integration
def test_task_create(client, session, test_user):
    category = make.a_category(session)
    todo_data = {
        "name": "task_test",
        "description": "description",
        "todoType": "TASK",
        "completionPoints": 1,
        "dueDate": "2019-03-02 22:48:05",
        "category": {
            "id": category.id
        },
        "tags": ["who", "knows"]
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
    assert create_data["todoType"] == "TASK"
    assert create_data["completionPoints"] == todo_data["completionPoints"]
    assert create_data["dueDate"] == "Sat, 02 Mar 2019 22:48:05 GMT"
    assert create_data["category"] == {'id': category.id, "name": "test", "color": "#FFF"}
    assert sorted(create_data["tags"]) == sorted(["who", "knows"])
    assert create_data["actions"] == []
    assert create_data["createdDate"] is not None
    assert create_data["modifiedDate"] is not None

    task_record = session.query(TaskRecord).get(create_data.get("todoId"))

    assert task_record is not None
    assert task_record.todo_id is not None
    assert task_record.todo_owner_id == test_user.get("user_id")
    assert task_record.name == todo_data["name"]
    assert task_record.description == todo_data["description"]
    assert task_record.todo_type == TodoType.TASK
    assert task_record.completion_points == todo_data["completionPoints"]
    assert task_record.due_date == datetime.datetime(2019, 3, 2, 22, 48, 5)
    assert task_record.category.id == category.id
    assert task_record.category.name == "test"
    assert task_record.category.color == "#FFF"
    assert len(task_record.tags) == 2
    for tag in task_record.tags:
        assert tag.name in ["who", "knows"]
    assert len(task_record.actions) == 0
    assert task_record.created_date is not None
    assert task_record.modified_date is not None


@pytest.mark.integration
def test_task_create_unauthorized(client, session, test_user):
    category = make.a_category(session)
    todo_data = {
        "name": "task_test",
        "todoOwnerId": "123",
        "description": "description",
        "todoType": "TASK",
        "completionPoints": 1,
        "dueDate": "2019-03-02 22:48:05",
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
    assert create_resp.status_code == 401


@pytest.mark.integration
def test_task_create_admin(client, session, test_admin):
    category = make.a_category(session)
    todo_data = {
        "name": "task_test",
        "todoOwnerId": "123",
        "description": "description",
        "todoType": "TASK",
        "completionPoints": 1,
        "dueDate": "2019-03-02 22:48:05",
        "category": {
            "id": category.id
        },
        "tags": ["who", "knows"]
    }

    make.a_category(session)

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
    assert create_data["todoType"] == "TASK"
    assert create_data["dueDate"] == "Sat, 02 Mar 2019 22:48:05 GMT"
    assert create_data["completionPoints"] == todo_data["completionPoints"]
    assert create_data["category"] == {'id': category.id, "name": "test", "color": "#FFF"}
    assert sorted(create_data["tags"]) == sorted(["who", "knows"])
    assert create_data["actions"] == []
    assert create_data["createdDate"] is not None
    assert create_data["modifiedDate"] is not None

    task_record = session.query(TaskRecord).get(create_data.get("todoId"))

    assert task_record is not None
    assert task_record.todo_id is not None
    assert task_record.todo_owner_id == "123"
    assert task_record.name == todo_data["name"]
    assert task_record.description == todo_data["description"]
    assert task_record.todo_type == TodoType.TASK
    assert task_record.completion_points == todo_data["completionPoints"]
    assert task_record.due_date == datetime.datetime(2019, 3, 2, 22, 48, 5)
    assert task_record.category.id == category.id
    assert task_record.category.name == "test"
    assert task_record.category.color == "#FFF"
    assert len(task_record.tags) == 2
    for tag in task_record.tags:
        assert tag.name in ["who", "knows"]
    assert len(task_record.actions) == 0
    assert task_record.created_date is not None
    assert task_record.modified_date is not None


@pytest.mark.integration
def test_task_read(client, session, test_user):
    task_record = make.a_task(
        session,
        todo_owner_id=test_user.get("user_id"),
        due_date=datetime.datetime(2019, 3, 2),
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")],
        actions=[make.an_action(session)]
    )

    fetch_resp = client.get('/todo/%s' % task_record.todo_id,
                            headers={'Authorization': test_user.get("token")})
    assert fetch_resp.status_code == 200

    fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

    assert fetch_data is not None
    assert fetch_data["todoId"] == task_record.todo_id
    assert fetch_data["todoOwnerId"] == task_record.todo_owner_id
    assert fetch_data["name"] == task_record.name
    assert fetch_data["description"] == task_record.description
    assert fetch_data["todoType"] == task_record.todo_type.name
    assert fetch_data["completionPoints"] == task_record.completion_points
    assert fetch_data["dueDate"] == "Sat, 02 Mar 2019 00:00:00 GMT"
    assert fetch_data["category"] == {'id': task_record.category_id, "name": "test", "color": "#FFF"}
    assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
    assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
    assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
    assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"


@pytest.mark.integration
def test_task_read_unauthorized(client, session, test_user):
    task_record = make.a_task(
        session,
        todo_owner_id="123",
        due_date=datetime.datetime(2019, 3, 2),
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")],
        actions=[make.an_action(session)]
    )

    fetch_resp = client.get('/todo/%s' % task_record.todo_id,
                            headers={'Authorization': test_user.get("token")})
    assert fetch_resp.status_code == 401


@pytest.mark.integration
def test_task_read_admin(client, session, test_admin):
    task_record = make.a_task(
        session,
        todo_owner_id="123",
        due_date=datetime.datetime(2019, 3, 2),
        tags=[make.a_tag(session, name="knows"),
              make.a_tag(session, name="who")],
        actions=[make.an_action(session)]
    )

    fetch_resp = client.get('/todo/%s' % task_record.todo_id,
                            headers={'Authorization': test_admin.get("token")})
    assert fetch_resp.status_code == 200

    fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

    assert fetch_data is not None
    assert fetch_data["todoId"] == task_record.todo_id
    assert fetch_data["todoOwnerId"] == task_record.todo_owner_id
    assert fetch_data["name"] == task_record.name
    assert fetch_data["description"] == task_record.description
    assert fetch_data["todoType"] == task_record.todo_type.name
    assert fetch_data["completionPoints"] == task_record.completion_points
    assert fetch_data["dueDate"] == "Sat, 02 Mar 2019 00:00:00 GMT"
    assert fetch_data["category"] == {'id': task_record.category_id, "name": "test", "color": "#FFF"}
    assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
    assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
    assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
    assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"


@pytest.mark.integration
def test_task_read_not_found(client, session, test_user):
    fetch_resp = client.get('/todo/%s' % "abc",
                            headers={'Authorization': test_user.get("token")})

    assert fetch_resp.status_code == 404

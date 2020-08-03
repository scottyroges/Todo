import datetime
import json

import pytest

from app.todo.domains.todo_type import TodoType
from app.utils import make
from app.model import (
    Task as TaskRecord
)


class TestGetAll:
    @pytest.mark.integration
    def test_todo_get_all(self, client, session, test_user):
        category_record = make.a_category(session)
        make.a_habit(
            session,
            todo_owner_id=test_user.get("user_id"),
            category=category_record
        )
        make.a_habit(
            session=session,
            todo_owner_id="123"
        )

        make.a_reoccur(
            session,
            todo_owner_id=test_user.get("user_id"),
            category=category_record
        )

        fetch_resp = client.get('/todos',
                                headers={'Authorization': test_user.get("token")})

        assert fetch_resp.status_code == 200

        fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

        assert len(fetch_data) == 2

    @pytest.mark.integration
    def test_todo_get_all_user_id_non_admin(self, client, session, test_user):
        category_record = make.a_category(session)
        make.a_habit(
            session,
            todo_owner_id=test_user.get("user_id"),
            category=category_record
        )

        make.a_habit(
            session,
            todo_owner_id="123"
        )

        make.a_reoccur(
            session,
            todo_owner_id=test_user.get("user_id"),
            category=category_record
        )

        fetch_resp = client.get('/todos/123',
                                headers={'Authorization': test_user.get("token")})

        assert fetch_resp.status_code == 401

    @pytest.mark.integration
    def test_todo_get_all_user_id_non_admin(self, client, session, test_admin):
        category_record = make.a_category(session)
        make.a_habit(
            session,
            todo_owner_id="456",
            category=category_record
        )

        make.a_habit(
            session,
            todo_owner_id="123"
        )

        make.a_reoccur(
            session,
            todo_owner_id="456",
            category=category_record
        )

        fetch_resp = client.get('/todos/456',
                                headers={'Authorization': test_admin.get("token")})

        assert fetch_resp.status_code == 200

        fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

        assert len(fetch_data) == 2


class TestUpdateToDifferentType:
    @pytest.mark.integration
    def test_update_todo_to_different_type(self, client, session, test_user):
        habit_record = make.a_habit(session, todo_owner_id=test_user.get("user_id"))

        fetch_resp = client.get('/todo/%s' % habit_record.todo_id,
                                headers={'Authorization': test_user.get("token")})
        assert fetch_resp.status_code == 200

        fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

        task_data = {
            "name": "task_test",
            "todoId": fetch_data["todoId"],
            "todoOwnerId": "123",
            "description": "description",
            "todoType": "TASK",
            "completionPoints": 1,
            "dueDate": "2019-03-02 22:48:05",
            "category": fetch_data["category"]
        }

        data = json.dumps(task_data)
        update_resp = client.put('/todo',
                                 data=data,
                                 headers={'Authorization': test_user.get("token")})

        assert update_resp.status_code == 200
        update_data = json.loads(update_resp.data.decode('utf-8'))

        assert update_data is not None
        assert update_data["todoId"] == habit_record.todo_id
        assert update_data["todoOwnerId"] == habit_record.todo_owner_id
        assert update_data["name"] == task_data["name"]
        assert update_data["description"] == task_data["description"]
        assert update_data["todoType"] == "TASK"
        assert update_data["dueDate"] == "Sat, 02 Mar 2019 22:48:05 GMT"
        assert update_data["completionPoints"] == task_data["completionPoints"]
        assert update_data["category"] == {'id': task_data["category"]["id"], "name": "test", "color": "#FFF"}
        assert update_data["actions"] == []
        assert update_data["createdDate"] is not None
        assert update_data["modifiedDate"] is not None

        task_record = session.query(TaskRecord).get(habit_record.todo_id)

        assert task_record is not None
        assert task_record.todo_id == habit_record.todo_id
        assert task_record.todo_owner_id == habit_record.todo_owner_id
        assert task_record.name == task_data["name"]
        assert task_record.description == task_data["description"]
        assert task_record.todo_type == TodoType.TASK
        assert task_record.completion_points == task_data["completionPoints"]
        assert task_record.due_date == datetime.datetime(2019, 3, 2, 22, 48, 5)
        assert task_record.category.id == habit_record.category_id
        assert task_record.category.name == "test"
        assert task_record.category.color == "#FFF"
        assert len(task_record.actions) == 0
        assert task_record.created_date is not None
        assert task_record.modified_date is not None

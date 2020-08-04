import json
import pytest

from app.model import (
    Habit as HabitRecord,

)
from app.todo.domains.todo_type import TodoType
from app.utils import make


class TestHabitCreate:
    @pytest.mark.integration
    def test_habit_create(self, client, session, test_user):
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
    def test_habit_create_no_category(self, client, session, test_user):
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
            "tags": ["who", "knows"]
        }

        data = json.dumps(todo_data)
        create_resp = client.post('/todo',
                                  data=data,
                                  headers={'Authorization': test_user.get("token")})
        assert create_resp.status_code == 200

        create_data = json.loads(create_resp.data.decode('utf-8'))
        assert create_data is not None

        assert create_data["category"] == {}

    @pytest.mark.integration
    def test_habit_create_unauthorized(self, client, session, test_user):
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
    def test_habit_create_admin(self, client, session, test_admin):
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


class TestHabitRead:
    @pytest.mark.integration
    def test_habit_read(self, client, session, test_user):
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
        assert fetch_data["actions"][0]["actionId"] is not None
        assert fetch_data["actions"][0]["actionDate"] == 'Sun, 24 Feb 2019 00:00:00 GMT'
        assert fetch_data["actions"][0]["points"] == 1
        assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
        assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"

    @pytest.mark.integration
    def test_habit_read_unauthorized(self, client, session, test_user):
        habit_record = make.a_habit(
            session,
            todo_owner_id="123",
            tags=[make.a_tag(session, name="knows"),
                  make.a_tag(session, name="who")],
            actions=[make.an_action(session)]
        )

        fetch_resp = client.get('/todo/%s' % habit_record.todo_id,
                                headers={'Authorization': test_user.get("token")})
        assert fetch_resp.status_code == 401

    @pytest.mark.integration
    def test_habit_read_admin(self, client, session, test_admin):
        habit_record = make.a_habit(
            session,
            todo_owner_id="123",
            tags=[make.a_tag(session, name="knows"),
                  make.a_tag(session, name="who")],
            actions=[make.an_action(session)]
        )

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
        assert fetch_data["actions"][0]["actionId"] is not None
        assert fetch_data["actions"][0]["actionDate"] == 'Sun, 24 Feb 2019 00:00:00 GMT'
        assert fetch_data["actions"][0]["points"] == 1
        assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
        assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"

    @pytest.mark.integration
    def test_habit_read_not_found(self, client, session, test_user):
        fetch_resp = client.get('/todo/%s' % "abc",
                                headers={'Authorization': test_user.get("token")})

        assert fetch_resp.status_code == 404


class TestHabitUpdate:
    @pytest.mark.integration
    def test_habit_update(self, client, session, test_user):
        habit_record = make.a_habit(
            session,
            todo_owner_id=test_user.get("user_id"),
            tags=[make.a_tag(session, name="knows"),
                  make.a_tag(session, name="who")],
            actions=[make.an_action(session)]
        )

        fetch_resp = client.get('/todo/%s' % habit_record.todo_id,
                                headers={'Authorization': test_user.get("token")})

        fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

        new_category = make.a_category(session, name="new category", color="#aa1133")

        fetch_data["name"] = "updated habit"
        fetch_data["completionPoints"] = 3
        fetch_data["frequency"] = 2
        fetch_data["buffer"] = {
            "bufferType": "WEEKS",
            "amount": 1
        }
        fetch_data["period"] = {
            "periodType": "MONTHS",
            "amount": 1
        }
        fetch_data["category"] = {
            "id": new_category.id
        }

        data = json.dumps(fetch_data)
        update_resp = client.put('/todo',
                                 data=data,
                                 headers={'Authorization': test_user.get("token")})
        assert update_resp.status_code == 200

        update_data = json.loads(update_resp.data.decode('utf-8'))
        assert update_data is not None
        assert update_data["todoId"] == habit_record.todo_id
        assert update_data["todoOwnerId"] == test_user.get("user_id")
        assert update_data["name"] == fetch_data["name"]
        assert update_data["description"] == habit_record.description
        assert update_data["todoType"] == "HABIT"
        assert update_data["pointsPer"] == habit_record.points_per
        assert update_data["completionPoints"] == fetch_data["completionPoints"]
        assert update_data["frequency"] == fetch_data["frequency"]
        assert update_data["period"] == {'amount': 1, 'periodType': 'MONTHS'}
        assert update_data["buffer"] == {'amount': 1, 'bufferType': 'WEEKS'}
        assert update_data["category"] == {'id': new_category.id,
                                           "name": new_category.name,
                                           "color": new_category.color}
        assert sorted(update_data["tags"]) == sorted(["who", "knows"])
        assert update_data["actions"] == []
        assert update_data["createdDate"] is not None
        assert update_data["modifiedDate"] is not None

        updated_habit_record = session.query(HabitRecord).get(habit_record.todo_id)

        assert updated_habit_record is not None
        assert updated_habit_record.todo_id == habit_record.todo_id
        assert updated_habit_record.todo_owner_id == test_user.get("user_id")
        assert updated_habit_record.name == fetch_data["name"]
        assert updated_habit_record.description == habit_record.description
        assert updated_habit_record.todo_type == TodoType.HABIT
        assert updated_habit_record.points_per == habit_record.points_per
        assert updated_habit_record.completion_points == fetch_data["completionPoints"]
        assert updated_habit_record.frequency == fetch_data["frequency"]
        assert updated_habit_record.period == {'amount': 1, 'periodType': 'MONTHS'}
        assert updated_habit_record.buffer == {'amount': 1, 'bufferType': 'WEEKS'}
        assert updated_habit_record.category.id == new_category.id
        assert updated_habit_record.category.name == new_category.name
        assert updated_habit_record.category.color == new_category.color
        assert len(updated_habit_record.tags) == 2
        for tag in updated_habit_record.tags:
            assert tag.name in ["who", "knows"]
        assert len(updated_habit_record.actions) == 0
        assert updated_habit_record.created_date is not None
        assert updated_habit_record.modified_date is not None

    @pytest.mark.integration
    def test_habit_update_unauthorized(self, client, session, test_user):
        habit_record = make.a_habit(
            session,
            todo_owner_id="123",
            tags=[make.a_tag(session, name="knows"),
                  make.a_tag(session, name="who")],
            actions=[make.an_action(session)]
        )

        new_category = make.a_category(session, name="new category", color="#aa1133")

        todo_data = {
            "name": "updated habit",
            "todoId": habit_record.todo_id,
            "todoOwnerId": "123",
            "description": "description",
            "todoType": "HABIT",
            "pointsPer": 1,
            "completionPoints": 3,
            "frequency": 2,
            "buffer": {
                "bufferType": "WEEKS",
                "amount": 1
            },
            "period": {
                "periodType": "MONTHS",
                "amount": 1
            },
            "category": {
                "id": new_category.id
            },
            "tags": ["who", "knows"]
        }

        data = json.dumps(todo_data)
        update_resp = client.put('/todo',
                                 data=data,
                                 headers={'Authorization': test_user.get("token")})

        assert update_resp.status_code == 401

    @pytest.mark.integration
    def test_habit_update_admin(self, client, session, test_admin):
        habit_record = make.a_habit(
            session,
            todo_owner_id="123",
            tags=[make.a_tag(session, name="knows"),
                  make.a_tag(session, name="who")],
            actions=[make.an_action(session)]
        )

        fetch_resp = client.get('/todo/%s' % habit_record.todo_id,
                                headers={'Authorization': test_admin.get("token")})

        fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

        new_category = make.a_category(session, name="new category", color="#aa1133")

        fetch_data["name"] = "updated habit"
        fetch_data["completionPoints"] = 3
        fetch_data["frequency"] = 2
        fetch_data["buffer"] = {
            "bufferType": "WEEKS",
            "amount": 1
        }
        fetch_data["period"] = {
            "periodType": "MONTHS",
            "amount": 1
        }
        fetch_data["category"] = {
            "id": new_category.id
        }

        data = json.dumps(fetch_data)
        update_resp = client.put('/todo',
                                 data=data,
                                 headers={'Authorization': test_admin.get("token")})
        assert update_resp.status_code == 200

        update_data = json.loads(update_resp.data.decode('utf-8'))
        assert update_data is not None
        assert update_data["todoId"] == habit_record.todo_id
        assert update_data["todoOwnerId"] == "123"
        assert update_data["name"] == fetch_data["name"]
        assert update_data["description"] == habit_record.description
        assert update_data["todoType"] == "HABIT"
        assert update_data["pointsPer"] == habit_record.points_per
        assert update_data["completionPoints"] == fetch_data["completionPoints"]
        assert update_data["frequency"] == fetch_data["frequency"]
        assert update_data["period"] == {'amount': 1, 'periodType': 'MONTHS'}
        assert update_data["buffer"] == {'amount': 1, 'bufferType': 'WEEKS'}
        assert update_data["category"] == {'id': new_category.id,
                                           "name": new_category.name,
                                           "color": new_category.color}
        assert sorted(update_data["tags"]) == sorted(["who", "knows"])
        assert update_data["actions"] == []
        assert update_data["createdDate"] is not None
        assert update_data["modifiedDate"] is not None

        updated_habit_record = session.query(HabitRecord).get(habit_record.todo_id)

        assert updated_habit_record is not None
        assert updated_habit_record.todo_id == habit_record.todo_id
        assert updated_habit_record.todo_owner_id == "123"
        assert updated_habit_record.name == fetch_data["name"]
        assert updated_habit_record.description == habit_record.description
        assert updated_habit_record.todo_type == TodoType.HABIT
        assert updated_habit_record.points_per == habit_record.points_per
        assert updated_habit_record.completion_points == fetch_data["completionPoints"]
        assert updated_habit_record.frequency == fetch_data["frequency"]
        assert updated_habit_record.period == {'amount': 1, 'periodType': 'MONTHS'}
        assert updated_habit_record.buffer == {'amount': 1, 'bufferType': 'WEEKS'}
        assert updated_habit_record.category.id == new_category.id
        assert updated_habit_record.category.name == new_category.name
        assert updated_habit_record.category.color == new_category.color
        assert len(updated_habit_record.tags) == 2
        for tag in updated_habit_record.tags:
            assert tag.name in ["who", "knows"]
        assert len(updated_habit_record.actions) == 0
        assert updated_habit_record.created_date is not None
        assert updated_habit_record.modified_date is not None

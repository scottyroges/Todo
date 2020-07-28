import datetime
import json

import pytest
from app.model import (
    Habit as HabitRecord,
    Reoccur as ReoccurRecord,
    Category as CategoryRecord,
    Tag as TagRecord,
    Action as ActionRecord
)
from app.todo.domains.todo_type import TodoType


class TestPerformActionHabit:
    def _create_habit(self, user_id):
        period = {
            'amount': 1,
            'periodType': 'WEEKS',
            'start': None
        }
        buffer = {
            'amount': 1,
            'bufferType': 'DAY_START'
        }
        tags = [TagRecord(name="who"), TagRecord(name="knows")]
        habit_record = HabitRecord(todo_id="abc",
                                   todo_owner_id=user_id,
                                   name="habit",
                                   description="description",
                                   todo_type=TodoType.HABIT,
                                   points_per=1,
                                   completion_points=1,
                                   frequency=1,
                                   period=period,
                                   buffer=buffer,
                                   category=CategoryRecord(id="abc", name="test", color="#FFF"),
                                   tags=tags,
                                   created_date=datetime.datetime(2019, 2, 24),
                                   modified_date=datetime.datetime(2019, 2, 24))
        return habit_record

    @pytest.mark.integration
    def test_action_create_for_habit(self, client, session, test_user):
        habit_record = self._create_habit(test_user.get("user_id"))
        session.add(habit_record)
        session.commit()

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": "1",
            "todoId": habit_record.todo_id
        }
        data = json.dumps(action_data)
        create_resp = client.post('/action',
                                  data=data,
                                  headers={'Authorization': test_user.get("token")})
        assert create_resp.status_code == 200

        create_data = json.loads(create_resp.data.decode('utf-8'))

        assert create_data is not None
        assert create_data["todoId"] is not None
        assert create_data["todoOwnerId"] == test_user.get("user_id")
        assert create_data["name"] == "habit"
        assert create_data["description"] == "description"
        assert create_data["todoType"] == "HABIT"
        assert create_data["pointsPer"] == 1
        assert create_data["completionPoints"] == 1
        assert create_data["frequency"] == 1
        assert create_data["period"] == {'amount': 1, 'periodType': 'WEEKS'}
        assert create_data["buffer"] == {'amount': 1, 'bufferType': 'DAY_START'}
        assert create_data["category"] == {'id': "abc", "name": "test", "color": "#FFF"}
        assert sorted(create_data["tags"]) == sorted(["who", "knows"])
        assert create_data["actions"] == [{'actionDate': 'Thu, 21 Feb 2019 12:02:05 GMT', 'points': '1'}]
        assert create_data["createdDate"] is not None
        assert create_data["modifiedDate"] is not None

        action_record = (session.query(ActionRecord)
            .filter(ActionRecord.todo_id == habit_record.todo_id)[0])
        assert action_record is not None
        assert action_record.id is not None
        assert action_record.todo_id == habit_record.todo_id
        assert action_record.action_date == datetime.datetime(2019, 2, 21, 12, 2, 5)
        assert action_record.points == 1

    @pytest.mark.integration
    def test_action_create_unauthorized(self, client, session, test_user):
        habit_record = self._create_habit("123")
        session.add(habit_record)
        session.commit()

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": "1",
            "todoId": habit_record.todo_id
        }
        data = json.dumps(action_data)
        create_resp = client.post('/action',
                                  data=data,
                                  headers={'Authorization': test_user.get("token")})
        assert create_resp.status_code == 401

    @pytest.mark.integration
    def test_action_create_admin(self, client, session, test_admin):
        habit_record = self._create_habit("123")
        session.add(habit_record)
        session.commit()

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": "1",
            "todoId": habit_record.todo_id
        }
        data = json.dumps(action_data)
        create_resp = client.post('/action',
                                  data=data,
                                  headers={'Authorization': test_admin.get("token")})
        assert create_resp.status_code == 200

        create_data = json.loads(create_resp.data.decode('utf-8'))

        assert create_data is not None
        assert create_data["todoId"] is not None
        assert create_data["todoOwnerId"] == "123"
        assert create_data["name"] == "habit"
        assert create_data["description"] == "description"
        assert create_data["todoType"] == "HABIT"
        assert create_data["pointsPer"] == 1
        assert create_data["completionPoints"] == 1
        assert create_data["frequency"] == 1
        assert create_data["period"] == {'amount': 1, 'periodType': 'WEEKS'}
        assert create_data["buffer"] == {'amount': 1, 'bufferType': 'DAY_START'}
        assert create_data["category"] == {'id': "abc", "name": "test", "color": "#FFF"}
        assert sorted(create_data["tags"]) == sorted(["who", "knows"])
        assert create_data["actions"] == [{'actionDate': 'Thu, 21 Feb 2019 12:02:05 GMT', 'points': '1'}]
        assert create_data["createdDate"] is not None
        assert create_data["modifiedDate"] is not None

        action_record = (session.query(ActionRecord)
            .filter(ActionRecord.todo_id == habit_record.todo_id)[0])
        assert action_record is not None
        assert action_record.id is not None
        assert action_record.todo_id == habit_record.todo_id
        assert action_record.action_date == datetime.datetime(2019, 2, 21, 12, 2, 5)
        assert action_record.points == 1


class TestPerformActionReoccur:
    def _create_reoccur(self, user_id):
        repeat = {
            'when': ["Sunday"],
            'repeatType': 'DAY_OF_WEEK'
        }
        tags = [TagRecord(name="who"), TagRecord(name="knows")]
        reoccur_record = ReoccurRecord(todo_id="abc",
                                       todo_owner_id=user_id,
                                       name="reoccur",
                                       description="description",
                                       todo_type=TodoType.REOCCUR,
                                       completion_points=1,
                                       required=False,
                                       repeat=repeat,
                                       category=CategoryRecord(id="abc", name="test", color="#FFF"),
                                       tags=tags,
                                       created_date=datetime.datetime(2019, 2, 24),
                                       modified_date=datetime.datetime(2019, 2, 24))
        return reoccur_record

    @pytest.mark.integration
    def test_action_create_for_reoccur(self, client, session, test_user):
        reoccur_record = self._create_reoccur(test_user.get("user_id"))
        session.add(reoccur_record)
        session.commit()

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": "1",
            "todoId": reoccur_record.todo_id
        }
        data = json.dumps(action_data)
        create_resp = client.post('/action',
                                  data=data,
                                  headers={'Authorization': test_user.get("token")})
        assert create_resp.status_code == 200

        create_data = json.loads(create_resp.data.decode('utf-8'))

        assert create_data is not None
        assert create_data["todoId"] is not None
        assert create_data["todoOwnerId"] == test_user.get("user_id")
        assert create_data["name"] == "reoccur"
        assert create_data["description"] == "description"
        assert create_data["todoType"] == "REOCCUR"
        assert create_data["completionPoints"] == 1
        assert create_data["repeat"] == {'when': ["Sunday"], 'repeatType': 'DAY_OF_WEEK'}
        assert create_data["required"] is False
        assert create_data["category"] == {'id': "abc", "name": "test", "color": "#FFF"}
        assert sorted(create_data["tags"]) == sorted(["who", "knows"])
        assert create_data["actions"] == [{'actionDate': 'Thu, 21 Feb 2019 12:02:05 GMT', 'points': '1'}]
        assert create_data["createdDate"] is not None
        assert create_data["modifiedDate"] is not None

        action_record = (session.query(ActionRecord)
            .filter(ActionRecord.todo_id == reoccur_record.todo_id)[0])
        assert action_record is not None
        assert action_record.id is not None
        assert action_record.todo_id == reoccur_record.todo_id
        assert action_record.action_date == datetime.datetime(2019, 2, 21, 12, 2, 5)
        assert action_record.points == 1

    @pytest.mark.integration
    def test_action_create_unauthorized(self, client, session, test_user):
        reoccur_record = self._create_reoccur("123")
        session.add(reoccur_record)
        session.commit()

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": "1",
            "todoId": reoccur_record.todo_id
        }
        data = json.dumps(action_data)
        create_resp = client.post('/action',
                                  data=data,
                                  headers={'Authorization': test_user.get("token")})
        assert create_resp.status_code == 401

    @pytest.mark.integration
    def test_action_create_admin(self, client, session, test_admin):
        reoccur_record = self._create_reoccur("123")
        session.add(reoccur_record)
        session.commit()

        action_data = {
            "actionDate": "2019-02-21 12:02:05",
            "points": "1",
            "todoId": reoccur_record.todo_id
        }
        data = json.dumps(action_data)
        create_resp = client.post('/action',
                                  data=data,
                                  headers={'Authorization': test_admin.get("token")})
        assert create_resp.status_code == 200

        create_data = json.loads(create_resp.data.decode('utf-8'))

        assert create_data is not None
        assert create_data["todoId"] is not None
        assert create_data["todoOwnerId"] == "123"
        assert create_data["name"] == "reoccur"
        assert create_data["description"] == "description"
        assert create_data["todoType"] == "REOCCUR"
        assert create_data["completionPoints"] == 1
        assert create_data["required"] is False
        assert create_data["repeat"] == {'when': ["Sunday"], 'repeatType': 'DAY_OF_WEEK'}
        assert create_data["category"] == {'id': "abc", "name": "test", "color": "#FFF"}
        assert sorted(create_data["tags"]) == sorted(["who", "knows"])
        assert create_data["actions"] == [{'actionDate': 'Thu, 21 Feb 2019 12:02:05 GMT', 'points': '1'}]
        assert create_data["createdDate"] is not None
        assert create_data["modifiedDate"] is not None

        action_record = (session.query(ActionRecord)
            .filter(ActionRecord.todo_id == reoccur_record.todo_id)[0])
        assert action_record is not None
        assert action_record.id is not None
        assert action_record.todo_id == reoccur_record.todo_id
        assert action_record.action_date == datetime.datetime(2019, 2, 21, 12, 2, 5)
        assert action_record.points == 1

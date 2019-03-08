import datetime
import json

import pytest

from app.model import (
    Habit as HabitRecord,
    Task as TaskRecord,
    Reoccur as ReoccurRecord,
    Category as CategoryRecord,
    Tag as TagRecord,
    Action as ActionRecord
)
from app.todo.domains.todo_type import TodoType


def _create_habit_record(todo_id="abc", user_id="123"):
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
    habit_record = HabitRecord(todo_id=todo_id,
                               todo_owner_id=user_id,
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
    return habit_record


class TestReadHabit:
    @pytest.mark.integration
    def test_habit_read(self, client, session, test_user):
        habit_record = _create_habit_record(user_id=test_user.get("user_id"))
        session.add(habit_record)
        session.commit()

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
        assert sorted(fetch_data["categories"]) == sorted(["test", "again"])
        assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
        assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
        assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
        assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"

    @pytest.mark.integration
    def test_habit_read_unauthorized(self, client, session, test_user):
        habit_record = _create_habit_record(user_id="123")
        session.add(habit_record)
        session.commit()

        fetch_resp = client.get('/todo/%s' % habit_record.todo_id,
                                headers={'Authorization': test_user.get("token")})
        assert fetch_resp.status_code == 401

    @pytest.mark.integration
    def test_habit_read_admin(self, client, session, test_admin):
        habit_record = _create_habit_record(user_id="123")
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
        assert sorted(fetch_data["categories"]) == sorted(["test", "again"])
        assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
        assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
        assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
        assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"

    @pytest.mark.integration
    def test_habit_read_not_found(self, client, session, test_user):
        fetch_resp = client.get('/todo/%s' % "abc",
                                headers={'Authorization': test_user.get("token")})

        assert fetch_resp.status_code == 404


def _create_reoccur_record(todo_id="abc", user_id="123"):
    repeat = {
        'when': ["Sunday"],
        'repeatType': 'DAY_OF_WEEK'
    }
    categories = [CategoryRecord(name="test"), CategoryRecord(name="again")]
    tags = [TagRecord(name="who"), TagRecord(name="knows")]
    actions = [ActionRecord(action_date=datetime.datetime(2019, 2, 24),
                            points=1)]
    reoccur_record = ReoccurRecord(todo_id=todo_id,
                                   todo_owner_id=user_id,
                                   name="reoccur",
                                   description="description",
                                   todo_type=TodoType.REOCCUR,
                                   completion_points=1,
                                   required=False,
                                   repeat=repeat,
                                   categories=categories,
                                   tags=tags,
                                   actions=actions,
                                   created_date=datetime.datetime(2019, 2, 24),
                                   modified_date=datetime.datetime(2019, 2, 24))
    return reoccur_record


class TestReadReoccur:
    @pytest.mark.integration
    def test_reoccur_read(self, client, session, test_user):
        reoccur_record = _create_reoccur_record(user_id=test_user.get("user_id"))
        session.add(reoccur_record)
        session.commit()

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
        assert sorted(fetch_data["categories"]) == sorted(["test", "again"])
        assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
        assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
        assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
        assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"

    @pytest.mark.integration
    def test_reoccur_read_unauthorized(self, client, session, test_user):
        reoccur_record = _create_reoccur_record(user_id="123")
        session.add(reoccur_record)
        session.commit()

        fetch_resp = client.get('/todo/%s' % reoccur_record.todo_id,
                                headers={'Authorization': test_user.get("token")})
        assert fetch_resp.status_code == 401

    @pytest.mark.integration
    def test_reoccur_read_admin(self, client, session, test_admin):
        reoccur_record = _create_reoccur_record(user_id="123")
        session.add(reoccur_record)
        session.commit()

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
        assert sorted(fetch_data["categories"]) == sorted(["test", "again"])
        assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
        assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
        assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
        assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"

    @pytest.mark.integration
    def test_reoccur_read_not_found(self, client, session, test_user):
        fetch_resp = client.get('/todo/%s' % "abc",
                                headers={'Authorization': test_user.get("token")})

        assert fetch_resp.status_code == 404


def _create_task_record(todo_id="abc", user_id="123"):
    categories = [CategoryRecord(name="test"), CategoryRecord(name="again")]
    tags = [TagRecord(name="who"), TagRecord(name="knows")]
    actions = [ActionRecord(action_date=datetime.datetime(2019, 2, 24),
                            points=1)]
    task_record = TaskRecord(todo_id=todo_id,
                             todo_owner_id=user_id,
                             name="task",
                             description="description",
                             todo_type=TodoType.TASK,
                             completion_points=1,
                             due_date=datetime.datetime(2019, 3, 2),
                             categories=categories,
                             tags=tags,
                             actions=actions,
                             created_date=datetime.datetime(2019, 2, 24),
                             modified_date=datetime.datetime(2019, 2, 24))
    return task_record

class TestReadTask:
    @pytest.mark.integration
    def test_task_read(self, client, session, test_user):
        task_record = _create_task_record(user_id=test_user.get("user_id"))
        session.add(task_record)
        session.commit()

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
        assert sorted(fetch_data["categories"]) == sorted(["test", "again"])
        assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
        assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
        assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
        assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"

    @pytest.mark.integration
    def test_task_read_unauthorized(self, client, session, test_user):
        task_record = _create_task_record(user_id="123")
        session.add(task_record)
        session.commit()

        fetch_resp = client.get('/todo/%s' % task_record.todo_id,
                                headers={'Authorization': test_user.get("token")})
        assert fetch_resp.status_code == 401

    @pytest.mark.integration
    def test_task_read_admin(self, client, session, test_admin):
        task_record = _create_task_record(user_id="123")
        session.add(task_record)
        session.commit()

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
        assert sorted(fetch_data["categories"]) == sorted(["test", "again"])
        assert sorted(fetch_data["tags"]) == sorted(["who", "knows"])
        assert fetch_data["actions"] == [{'actionDate': 'Sun, 24 Feb 2019 00:00:00 GMT', "points": 1}]
        assert fetch_data["createdDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"
        assert fetch_data["modifiedDate"] == "Sun, 24 Feb 2019 00:00:00 GMT"

    @pytest.mark.integration
    def test_task_read_not_found(self, client, session, test_user):
        fetch_resp = client.get('/todo/%s' % "abc",
                                headers={'Authorization': test_user.get("token")})

        assert fetch_resp.status_code == 404


class TestGetAll:
    @pytest.mark.integration
    def test_todo_get_all(self, client, session, test_user):
        habit1 = _create_habit_record(user_id=test_user.get("user_id"))
        session.add(habit1)
        habit2 = _create_habit_record(todo_id="def", user_id="123")
        session.add(habit2)
        reoccur1 = _create_reoccur_record(todo_id="hij", user_id=test_user.get("user_id"))
        session.add(reoccur1)
        session.commit()

        fetch_resp = client.get('/todos',
                                headers={'Authorization': test_user.get("token")})

        assert fetch_resp.status_code == 200

        fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

        assert len(fetch_data) == 2

    @pytest.mark.integration
    def test_todo_get_all_user_id_non_admin(self, client, session, test_user):
        habit1 = _create_habit_record(user_id=test_user.get("user_id"))
        session.add(habit1)
        habit2 = _create_habit_record(todo_id="def", user_id="123")
        session.add(habit2)
        reoccur1 = _create_reoccur_record(todo_id="hij", user_id=test_user.get("user_id"))
        session.add(reoccur1)
        session.commit()

        fetch_resp = client.get('/todos/123',
                                headers={'Authorization': test_user.get("token")})

        assert fetch_resp.status_code == 401

    @pytest.mark.integration
    def test_todo_get_all_user_id_non_admin(self, client, session, test_admin):
        habit1 = _create_habit_record(user_id="456")
        session.add(habit1)
        habit2 = _create_habit_record(todo_id="def", user_id="123")
        session.add(habit2)
        reoccur1 = _create_reoccur_record(todo_id="hij", user_id="456")
        session.add(reoccur1)
        session.commit()

        fetch_resp = client.get('/todos/456',
                                headers={'Authorization': test_admin.get("token")})

        assert fetch_resp.status_code == 200

        fetch_data = json.loads(fetch_resp.data.decode('utf-8'))

        assert len(fetch_data) == 2


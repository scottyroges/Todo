import json

import pytest

from app.utils import make


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

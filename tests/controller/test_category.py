import json

import pytest

from app.model import Category
from app.utils import make


@pytest.mark.integration
def test_category_create(client, session, test_user):
    category_data = {
        "name": "test",
        "color": "#FFF"
    }

    data = json.dumps(category_data)
    create_resp = client.post('/category',
                              data=data,
                              headers={'Authorization': test_user.get("token")})
    assert create_resp.status_code == 200

    create_data = json.loads(create_resp.data.decode('utf-8'))
    assert create_data is not None
    assert create_data["id"] is not None
    assert create_data["name"] == category_data["name"]
    assert create_data["color"] == category_data["color"]

    category_record = session.query(Category).get(create_data.get("id"))

    assert category_record is not None
    assert category_record.id is not None
    assert category_record.name == category_data["name"]
    assert category_record.color == category_data["color"]


@pytest.mark.integration
def test_category_create_unauthorized(client, session, test_user):
    category_data = {
        "userId": "123",
        "name": "test",
        "color": "#FFF"
    }
    data = json.dumps(category_data)
    create_resp = client.post('/category',
                              data=data,
                              headers={'Authorization': test_user.get("token")})
    assert create_resp.status_code == 401


@pytest.mark.integration
def test_category_create_admin(client, session, test_admin):
    category_data = {
        "name": "test",
        "color": "#FFF"
    }
    data = json.dumps(category_data)
    create_resp = client.post('/category',
                              data=data,
                              headers={'Authorization': test_admin.get("token")})
    assert create_resp.status_code == 200

    create_data = json.loads(create_resp.data.decode('utf-8'))
    assert create_data is not None
    assert create_data["id"] is not None
    assert create_data["name"] == category_data["name"]
    assert create_data["color"] == category_data["color"]

    category_record = session.query(Category).get(create_data.get("id"))

    assert category_record is not None
    assert category_record.id is not None
    assert category_record.name == category_data["name"]
    assert category_record.color == category_data["color"]


@pytest.mark.integration
def test_category_get_categories(client, session, test_user):
    make.a_category(session, user_id=test_user.get("user_id"))
    read_resp = client.get('/categories',
                           headers={'Authorization': test_user.get("token")})

    assert read_resp.status_code == 200

    read_data = json.loads(read_resp.data.decode('utf-8'))

    assert len(read_data) == 1
    assert read_data[0]['id'] is not None
    assert read_data[0]['name'] == "test"
    assert read_data[0]['color'] == "#FFF"

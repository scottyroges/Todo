import sys
from unittest.mock import Mock

import pytest

from app.utils.attrdict import AttrDict


@pytest.fixture()
def pre_auth_request(mocker):
    request = AttrDict({})

    mocker.patch("app.auth.get_request._get_request",
                 new=lambda: request)
    return request


@pytest.fixture()
def user_request(mocker):
    request = AttrDict({
        "user_id": "123"
    })
    mocker.patch("app.auth.get_request._get_request",
                 new=lambda: request)
    return request


@pytest.fixture()
def admin_request(mocker):
    request = AttrDict({
        "user_id": "123",
        "groups": [
            "Admin"
        ]
    })

    mocker.patch("app.auth.get_request._get_request",
                 new=lambda: request)
    return request

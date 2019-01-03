import pytest

from app.auth.auth_decorator import authorized
from app.auth.token_decode import InvalidToken
from app.errors import UnauthorizedError


def test_authorized_wrapper_valid(pre_auth_request, mocker):
    mock_ar = mocker.patch("app.auth.auth_decorator.authorize_request")
    mock_ar.return_value = {
        "sub": "123"
    }

    @authorized
    def func():
        return 1

    assert func() == 1
    assert pre_auth_request.user_id == "123"
    assert pre_auth_request.groups == []


def test_authorized_wrapper_valid_admin(pre_auth_request, mocker):
    mock_ar = mocker.patch("app.auth.auth_decorator.authorize_request")
    mock_ar.return_value = {
        "sub": "123",
        "cognito:groups": [
            "Admin"
        ]
    }

    @authorized
    def func():
        return 1

    assert func() == 1
    assert pre_auth_request.user_id == "123"
    assert "Admin" in pre_auth_request.groups


def test_authorized_wrapper_invalid(mocker):
    mock_ar = mocker.patch("app.auth.auth_decorator.authorize_request")
    mock_ar.side_effect = InvalidToken

    @authorized
    def func():
        return 1

    with pytest.raises(UnauthorizedError):
        func()

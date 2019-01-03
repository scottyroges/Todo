from app.auth.auth_util import (
    is_owner,
    is_admin,
    is_owner_or_admin
)


def test_is_owner_true(user_request):
    assert is_owner("123") is True


def test_is_owner_false(user_request):
    assert is_owner("321") is False


def test_is_admin_true(admin_request):
    assert is_admin() is True


def test_is_admin_false(user_request):
    assert is_admin() is False


def test_is_owner_or_admin_true_user(user_request):
    assert is_owner_or_admin("123") is True


def test_is_owner_or_admin_false_user(user_request):
    assert is_owner_or_admin("321") is False


def test_is_owner_or_admin_true_admin(admin_request):
    assert is_owner_or_admin("123") is True
    assert is_owner_or_admin("321") is True



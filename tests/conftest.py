import pytest

from app.utils.attrdict import AttrDict


def pytest_addoption(parser):
    parser.addoption("--integration", action="store_true", help="run integration tests")
    parser.addoption("--all", action="store_true", help="run all tests")


def pytest_runtest_setup(item):
    """
    Only run tests marked with 'integration' when --integration is passed
    """
    run_integration = item.config.getoption("--integration")

    run_all = item.config.getoption("--all")
    if not run_all:
        if run_integration and 'integration' not in item.keywords:
            pytest.skip("skipping test not marked as integration")
        elif 'integration' in item.keywords and not run_integration:
            pytest.skip("pass --integration option to pytest to run this test")


@pytest.fixture()
def pre_auth_request(mocker):
    request = AttrDict({})

    mocker.patch("app.auth._get_request",
                 new=lambda: request)
    return request


@pytest.fixture()
def user_request(mocker):
    request = AttrDict({
        "user_id": "123"
    })
    mocker.patch("app.auth._get_request",
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

    mocker.patch("app.auth._get_request",
                 new=lambda: request)
    return request

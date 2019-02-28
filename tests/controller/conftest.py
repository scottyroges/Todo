import boto3
import pytest

from app.app import create_app
from app.config import config
from app.database import db


# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
#     client = app.test_client()
#
#     yield client
#
#
# @pytest.fixture(scope='function')
# def session():
#     return
#     # """Creates a new database session for a test."""
#     # connection = db.engine.connect()
#     # transaction = connection.begin()
#     #
#     # options = dict(bind=connection, binds={})
#     # session = db.create_scoped_session(options=options)
#     #
#     # db.session = session
#     #
#     # yield session
#     #
#     # transaction.rollback()
#     # connection.close()
#     # session.remove()
from app.utils.helper_methods import get_hmac_digest


@pytest.fixture(scope='session')
def client(request):
    """Session-wide test `Flask` application."""
    app = create_app()
    app.config['TESTING'] = True

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app.test_client()


@pytest.fixture(scope='function')
def session(request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='session')
def test_user():
    client = boto3.client('cognito-idp', config.get("cognitoRegion"))
    resp = client.admin_initiate_auth(
        UserPoolId=config.get("cognitoUserPoolId"),
        ClientId=config.get("cognitoClientId"),
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": "test_user",
            'PASSWORD': config.get("test_user_password"),
            "SECRET_HASH": get_hmac_digest("test_user")
        })
    return {
        "token": resp.get("AuthenticationResult").get("AccessToken"),
        "user_id": config.get("test_user_id")
    }


@pytest.fixture(scope='session')
def test_admin():
    client = boto3.client('cognito-idp', config.get("cognitoRegion"))
    resp = client.admin_initiate_auth(
        UserPoolId=config.get("cognitoUserPoolId"),
        ClientId=config.get("cognitoClientId"),
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": "test_admin",
            'PASSWORD': config.get("test_admin_password"),
            "SECRET_HASH": get_hmac_digest("test_admin")
        })
    return {
        "token": resp.get("AuthenticationResult").get("AccessToken"),
        "user_id": config.get("test_admin_id")
    }

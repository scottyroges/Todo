import pytest

from app.app import create_app
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
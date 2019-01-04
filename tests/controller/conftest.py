import pytest
from app.server import app, db


@pytest.fixture
def client():

    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@pytest.fixture(scope='function')
def session():
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


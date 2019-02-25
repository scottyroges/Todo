import pytest


@pytest.fixture
def client():
    return
    # app.config['TESTING'] = True
    # client = app.test_client()
    #
    # yield client


@pytest.fixture(scope='function')
def session():
    return
    # """Creates a new database session for a test."""
    # connection = db.engine.connect()
    # transaction = connection.begin()
    #
    # options = dict(bind=connection, binds={})
    # session = db.create_scoped_session(options=options)
    #
    # db.session = session
    #
    # yield session
    #
    # transaction.rollback()
    # connection.close()
    # session.remove()


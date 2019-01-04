from app.errors import AppError, UnauthorizedError, MarshallingError


def test_app_error():
    error = AppError(message="my error")
    assert error.to_dict() == {
        "statusCode": 400,
        "message": "AppError: my error"
    }


def test_app_error_no_message():
    error = AppError()
    assert error.to_dict() == {
        "statusCode": 400,
        "message": "Error: AppError"
    }


def test_app_error_status_code():
    error = AppError(status_code=490)
    assert error.to_dict() == {
        "statusCode": 490,
        "message": "Error: AppError"
    }


def test_app_error_payload():
    error = AppError(payload={"prop": "prop1"})
    assert error.to_dict() == {
        "statusCode": 400,
        "message": "Error: AppError",
        "prop": "prop1"
    }


class FakeError(AppError):
    pass


def test_app_error_subclass_no_message():
    error = FakeError(message="my error")
    assert error.to_dict() == {
        "statusCode": 400,
        "message": "FakeError: my error"
    }


def test_app_error_subclass_no_message():
    error = FakeError()
    assert error.to_dict() == {
        "statusCode": 400,
        "message": "Error: FakeError"
    }


def test_unauthorized_error():
    error = UnauthorizedError()
    assert error.to_dict() == {
        "statusCode": 401,
        "message": "Error: UnauthorizedError"
    }


def test_marshalling_error():
    error = MarshallingError()
    assert error.to_dict() == {
        "statusCode": 400,
        "message": "Error: MarshallingError"
    }

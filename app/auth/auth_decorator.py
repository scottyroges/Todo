from functools import wraps
from app.auth import get_request
from app.auth.token_decode import authorize_request, InvalidTokenError
from app.errors import UnauthorizedError


def authorized(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            request = get_request()
            claims = authorize_request(request)
            request.user_id = claims.get("sub", None)
            request.groups = claims.get("cognito:groups", [])
        except InvalidTokenError as e:
            raise UnauthorizedError(e.message)
        return f(*args, **kwargs)
    return wrapper

from functools import wraps
from app.auth.get_request import get_request
from app.auth.token_decode import authorize_request, InvalidToken
from app.errors import UnauthorizedError


def authorized(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            request = get_request()
            claims = authorize_request(request)
            request.user_id = claims.get("sub", None)
            request.groups = claims.get("cognito:groups", [])
        except InvalidToken as e:
            raise UnauthorizedError(e.message)
        return f(*args, **kwargs)
    return wrapper

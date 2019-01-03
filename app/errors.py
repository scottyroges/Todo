class AppError(Exception):
    status_code = 400
    prefix = "Error"

    def __init__(self, message="", status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['statusCode'] = self.status_code
        rv['message'] = "%s: %s" % (self.prefix, self.message)
        return rv


class UnauthorizedError(AppError):
    status_code = 401
    prefix = "Unauthorized Request"


class MarshallingError(AppError):
    status_code = 400
    prefix = "Marshalling Error"

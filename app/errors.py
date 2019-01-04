class AppError(Exception):
    status_code = 400

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        response = dict(self.payload or ())
        response['statusCode'] = self.status_code
        if self.message is not None:
            response['message'] = "%s: %s" % (self.__class__.__name__, self.message)
        else:
            response['message'] = "%s: %s" % ("Error", self.__class__.__name__)
        return response


class UnauthorizedError(AppError):
    status_code = 401


class MarshallingError(AppError):
    pass


class NotFoundError(AppError):
    status_code = 404

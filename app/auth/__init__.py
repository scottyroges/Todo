from flask import request


def _get_request():
    # this provides an abstraction for easier testing
    # we could also make a request object of our own
    # so that we can change to a different server if we want
    return request


def get_request():
    return _get_request()

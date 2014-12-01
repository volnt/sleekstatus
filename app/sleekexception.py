"""
SleekException module

Contains the SleekException and the catch_sleekexception decorator
"""
from functools import wraps
from flask import make_response, jsonify


def catch_sleekexception(function):
    """
    Decorator catching sleekexceptions
    """
    @wraps(function)
    def wrapped(*args, **kwargs):
        """
        Throws an error if a sleekexception is caught
        """
        try:
            ret = function(*args, **kwargs)
        except SleekException as e:
            return make_response(jsonify({
                "error": e.message
            }), e.status_code)
        else:
            return ret
    return wrapped


class SleekException(Exception):
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

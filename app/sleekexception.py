"""
SleekException module

Contains the SleekException and the catch_sleekexception decorator
"""
from functools import wraps
from flask import make_response, jsonify
from stripe.error import CardError, InvalidRequestError, AuthenticationError
from stripe.error import APIConnectionError, StripeError


def catch_sleekexception(function):
    """
    Decorator catching SleekException and Stripe exceptions.
    
    It propagates the exceptions as clean json responses.
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
        except (CardError, InvalidRequestError, AuthenticationError,
                APIConnectionError, StripeError) as e:
            return make_response(jsonify({
                "error": e.message
            }), e.http_status)            
        else:
            return ret
    return wrapped


class SleekException(Exception):
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

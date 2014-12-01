"""
is_authenticated module

Contains the is_authenticated decorator
"""
from functools import wraps
from flask import make_response, session, jsonify


def is_authenticated(function):
    """
    Decorator checking if the user is connected.

    If he's not it'll throw an error 401.
    """
    @wraps(function)
    def wrapped(*args, **kwargs):
        """
        Return current user if connected else throws a 401 error
        """
        from app.api import User
        email, password = session.get("email"), session.get("password")
        if not User.valid_auth(email, password):
            return make_response(jsonify({
                'error': 'Authentication needed.'
            }), 401)
        return function(User(email, password), *args, **kwargs)
    return wrapped

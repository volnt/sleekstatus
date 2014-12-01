"""
is_authenticated module

Contains the is_authenticated decorator
"""
from functools import wraps
from flask import session


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
        user = User.login(email, password)
        return function(user, *args, **kwargs)
    return wrapped

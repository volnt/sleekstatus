from functools import wraps
from flask import make_response, session, jsonify

def is_authenticated(f):
    """
    Decorator checking if the user is connected.

    If he's not it'll throw an error 400.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        from app.api import User
        email, password = session.get("email"), session.get("password")
        if not User.valid_auth(email, password):
            return make_response(jsonify({'error': 'Authentication needed.'}), 401)
        return f(user=User(email, password), *args, **kwargs)
    return wrapped


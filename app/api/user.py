from functools import wraps
from app import app, redis
from hashlib import sha1
from flask import jsonify, make_response, abort, request, session

def is_authenticated(f):
    """
    Decorator checking if the user is connected.

    If he's not it'll throw an error 400.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        email, password = session.get("email"), session.get("password")
        if not User.valid_auth(email, password):
            return make_response(jsonify({'error': 'Authentication needed.'}), 401)
        return f(user=User(email, password), *args, **kwargs)
    return wrapped

class User(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def register(self):
        sha = sha1(self.email).hexdigest()

        return (redis.sadd("sl:account:ids", sha) and
                redis.hmset("sl:account:{}".format(sha), self.to_dict()))

    @staticmethod
    def valid_auth(email, password):
        if not email or not password:
            return False
        sha = sha1(email).hexdigest()
        user_info = redis.hgetall("sl:account:{}".format(sha))

        return user_info and user_info.get("password") == password

    @classmethod
    def login(cls, email, password):
        """
        This method will not only login but also register new users

        First if the user is known and the passwords match we login
        the user. Then if it's unknown we register him and if the
        user is known but the passwords don't match we return None.
        """
        sha = sha1(email).hexdigest()
        user = cls(email, password)

        if cls.valid_auth(email, password):
            session["email"], session["password"] = email, password
            return user
        elif user.register():
            return user
        else:
            return None

    def to_dict(self):
        return {"email": self.email, "password": self.password }

@app.route('/api/user/login', methods=['POST'])
def user_login():
    if not request.json:
        return abort(400)
    user = User.login(request.json.get("email"), request.json.get("password"))

    if user:
        return make_response(jsonify(user.to_dict()))
    else:
        return make_response(jsonify({"error": "Incorrect password."}), 400)

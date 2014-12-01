"""
User module

Contains the User class and the associated API endpoints.
"""
from app import app, redis
from app.api import Plan
from app.utils import str_to_none
from hashlib import sha1
from flask import jsonify, make_response, request, session


class User(object):
    """
    User class

    Represent a user with an email and a password.
    """
    def __init__(self, email, password):
        """
        Returns a user from email and password
        """
        self.email = email
        self.password = password

        self._set_user_info(password)

    def _set_user_info(self, password):
        """
        Fetch and set current user infos based on the informations stored
        in the database.
        """
        sha = sha1(self.email).hexdigest()
        user_info = redis.hgetall("sl:account:{}".format(sha))

        if type(user_info) != dict or user_info.get("password") != password:
            user_info = {}

        self.plan = Plan.from_id(user_info.get("plan"))
        self.customer_token = str_to_none(
            user_info.get("customer_token")
        )
        self.subscription_token = str_to_none(
            user_info.get("subscription_token")
        )
        self.subscription_end = str_to_none(
            user_info.get("subscription_end")
        )

    def save(self):
        """
        Save the current user infos to database.
        """
        sha = sha1(self.email).hexdigest()
        infos = self.to_dict()
        infos["plan"] = infos["plan"]["id"] if infos["plan"] else None

        return bool(redis.hmset("sl:account:{}".format(sha), infos))

    def register(self):
        """
        Register and save the current user to database.
        """
        sha = sha1(self.email).hexdigest()

        return bool(redis.sadd("sl:account:ids", sha) and self.save())

    @staticmethod
    def valid_auth(email, password):
        """
        Return True if user exists and the credentials are right.
        Return False otherwise.
        """
        if not email or not password:
            return False
        sha = sha1(email).hexdigest()
        user_info = redis.hgetall("sl:account:{}".format(sha))

        return bool(
            type(user_info) == dict and
            user_info.get("password") == password
        )

    @classmethod
    def login(cls, email, password):
        """
        This method will not only login but also register new users

        First if the user is known and the passwords match we login
        the user. Then if it's unknown we register him and if the
        user is known but the passwords don't match we return None.
        """
        user = cls(email, password)

        if User.valid_auth(email, password) or user.register():
            return user
        else:
            return None

    def to_dict(self):
        """
        Return an dict representation of the current user
        """
        return {
            "email": self.email,
            "password": self.password,
            "plan": self.plan.to_dict() if self.plan else None,
            "customer_token": self.customer_token,
            "subscription_token": self.subscription_token,
            "subscription_end": self.subscription_end
        }


@app.route('/api/user/login', methods=['POST'])
def user_login():
    """
    Try to login user based on email and password
    """
    if not request.json:
        return make_response(jsonify({"error": "Incorrect parameters."}), 400)
    user = User.login(request.json.get("email"), request.json.get("password"))

    if user:
        session["email"], session["password"] = user.email, user.password
        return make_response(jsonify(user.to_dict()))
    else:
        return make_response(jsonify({"error": "Incorrect password."}), 401)

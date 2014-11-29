from app import app, redis
from app.api import Plan
from app.utils import str_to_none
from hashlib import sha1
from flask import jsonify, make_response, abort, request, session

class User(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

        self._set_user_info(password)

    def _set_user_info(self, password):
        sha = sha1(self.email).hexdigest()
        user_info = redis.hgetall("sl:account:{}".format(sha))

        if not user_info or not user_info.get("password") == password:
            user_info = {}

        self.plan = Plan.from_id(user_info.get("plan"))
        self.customer_token = user_info.get("customer_token")
        self.customer_token = str_to_none(self.customer_token)
        self.subscription_end = user_info.get("subscription_end")
        self.subscription_end = str_to_none(self.subscription_end)

    def save(self):
        sha = sha1(self.email).hexdigest()

        return redis.hmset("sl:account:{}".format(sha), self.to_dict())

    def register(self):
        sha = sha1(self.email).hexdigest()

        return redis.sadd("sl:account:ids", sha) and self.save()

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
        return {
            "email": self.email, 
            "plan": self.plan._id if self.plan else None,
            "customer_token": self.customer_token,
            "subscription_end": self.subscription_end
        }

@app.route('/api/user/login', methods=['POST'])
def user_login():
    if not request.json:
        return abort(400)
    user = User.login(request.json.get("email"), request.json.get("password"))

    if user:
        return make_response(jsonify(user.to_dict()))
    else:
        return make_response(jsonify({"error": "Incorrect password."}), 400)

from app import redis, app, mode
from app.api import Plan, User
from flask import session, request
from mock import patch, MagicMock
from hashlib import sha1
import json
app.testing = True

assert mode == "TEST"

class TestUserAPI(object):
    def setup(self):
        redis.flushdb()
        self.user = User("user@host.ndd", "password")
        self.sha = sha1(self.user.email).hexdigest()
        self.client = app.test_client()

    def test_user_register(self):
        """
        It should register the user when the email is not in database.
        """
        res = self.client.post("/api/user/login", data=json.dumps({
            "email": self.user.email,
            "password": self.user.password
        }), content_type="application/json")

        assert res.status_code == 200
        assert json.loads(res.data) == self.user.to_dict()

    def test_user_login(self):
        """
        It should login the user when the email is in database and the 
        password match the one stored in database.
        """
        assert self.user.register() is True
        res = self.client.post("/api/user/login", data=json.dumps({
            "email": self.user.email,
            "password": self.user.password
        }), content_type="application/json")

        assert res.status_code == 200
        assert json.loads(res.data) == self.user.to_dict()        

    def test_user_bad_credentials(self):
        """
        It should return an error 401 when the user submits the wrong 
        credentials.
        """
        assert self.user.register() is True
        res = self.client.post("/api/user/login", data=json.dumps({
            "email": self.user.email,
            "password": "wrong"
        }), content_type="application/json")

        assert res.status_code == 401
        assert json.loads(res.data)["error"]

class TestUser(object):
    def setup(self):
        redis.flushdb()
        self.user = User("user@host.ndd", "password")
        self.sha = sha1(self.user.email).hexdigest()

    @patch.object(Plan, "from_id")
    def test_init_user(self, from_id):
        """
        It should fill the plan, customer_token, subscription_token and 
        subscription_end attributs with what's stored in database when 
        instantiating a User object.
        """
        self.user.plan = MagicMock()
        self.user.customer_token = "customer_token"
        self.user.subscription_token = "subscription_token"
        self.user.subscription_end = "subscription_end"

        assert self.user.register() is True

        user = User(self.user.email, self.user.password)
        from_id.assert_called_once_with(str(self.user.plan.to_dict()["id"]))
        assert user.plan == from_id.return_value
        assert user.customer_token == self.user.customer_token
        assert user.subscription_token == self.user.subscription_token
        assert user.subscription_end == self.user.subscription_end
        

    def test_save(self):
        """
        It should save the user infos in database when calling the User.save
        method.
        """
        assert self.user.save() is True
        assert redis.hgetall("sl:account:{}".format(self.sha))

    def test_register(self):
        """
        It should add a user id to the account list in database and save the
        user to database when calling the User.register method.
        """
        assert self.user.register() is True
        assert redis.sismember("sl:account:ids", self.sha) is True
        assert redis.hgetall("sl:account:{}".format(self.sha))

    def test_valid_auth(self):
        """
        It should return True if the credentials are valid when calling the 
        User.valid_auth staticmethod.
        """
        assert self.user.register() is True
        assert User.valid_auth(self.user.email, self.user.password) is True

    def test_invalid_auth(self):
        """
        It should return False if the credentials are invalid when calling the
        User.valid_auth staticmethod.
        """
        assert self.user.register() is True
        assert User.valid_auth(self.user.email, "wrong") is False

    def test_login_existing_user(self):
        """
        It should login an existing user when calling the User.login classmethod.
        """
        assert self.user.register() is True
        assert User.login(self.user.email, self.user.password) is not None
    
    def test_login_new_user(self):
        """
        It should register and login a new user when calling the User.login classmethod.
        """
        assert User.login(self.user.email, self.user.password) is not None
        assert redis.sismember("sl:account:ids", self.sha) is True
        assert redis.hgetall("sl:account:{}".format(self.sha))

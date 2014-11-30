from app import redis, app
from flask import session, request
from mock import patch, MagicMock
from hashlib import sha1
import json
import app.api.alert as alert
import app.api.user as user
rns = "test:"
user.rns = rns
app.testing = True

class TestUserAPI(object):
    def setup(self):
        self.u = user.User("user@host.ndd", "password")
        self.sha = sha1(self.u.email).hexdigest()
        self.client = app.test_client()

    def clear_user(self):
        for key in self.u.to_dict():
            redis.hdel(rns+"account:{}".format(self.sha), key)
        redis.srem(rns+"account:ids", self.sha)

    def test_user_register(self):
        self.clear_user()

        res = self.client.post("/api/user/login", data=json.dumps({
            "email": self.u.email,
            "password": self.u.password
        }), content_type="application/json")

        assert res.status_code == 200
        assert json.loads(res.data) == self.u.to_dict()

    def test_user_login(self):
        self.clear_user()

        assert self.u.register() is True
        res = self.client.post("/api/user/login", data=json.dumps({
            "email": self.u.email,
            "password": self.u.password
        }), content_type="application/json")

        assert res.status_code == 200
        assert json.loads(res.data) == self.u.to_dict()        

    def test_user_bad_credentials(self):
        self.clear_user()

        assert self.u.register() is True
        res = self.client.post("/api/user/login", data=json.dumps({
            "email": self.u.email,
            "password": "wrong"
        }), content_type="application/json")

        assert res.status_code == 401
        assert json.loads(res.data)["error"]

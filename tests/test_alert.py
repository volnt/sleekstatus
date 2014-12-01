from app import redis, app, mode
from app.api import Alert, User, Plan
from flask import request
from mock import patch, MagicMock
from hashlib import sha1
import json
app.testing = True

assert mode == "TEST"

class TestAlertAPI(object):
    def setup(self):
        redis.flushdb()
        self.user = User("user@host.ndd", "password")
        self.alert = Alert("user@host.ndd", "http://host.ndd/path")
        self.sha = sha1(self.alert.email).hexdigest()
        self.client = app.test_client()

    def test_create_alert_unauthenticated(self):
        """
        It should return an error 401 if the user is not logged in.
        """
        res = self.client.post("/api/alert")

        assert res.status_code == 401
        assert json.loads(res.data)["error"]

    def test_create_alert(self):
        """
        It should create an alert for the current user if it has a big 
        enough plan to create one more alert.
        """
        with self.client.session_transaction() as session:
            res = self.client.post("/api/user/login", data=json.dumps({
                "email": self.user.email,
                "password": self.user.password
            }), content_type="application/json")
            self.user.plan = Plan(_id="basic", name="Basic", price=0, alert_number=3)
            self.user.save()
            res = self.client.post("/api/alert", data=json.dumps({
                "email": self.user.email,
                "url": self.alert.url
            }), content_type="application/json")

        assert res.status_code == 200
        assert json.loads(res.data) == self.alert.to_dict()
    
    def test_create_too_many_alert(self):
        """
        It should return an error to the current user if it doesn't
        have a big enough plan to create one more alert.
        """
        with self.client.session_transaction() as session:
            res = self.client.post("/api/user/login", data=json.dumps({
                "email": self.user.email,
                "password": self.user.password
            }), content_type="application/json")
            res = self.client.post("/api/alert", data=json.dumps({
                "email": self.user.email,
                "url": self.alert.url
            }), content_type="application/json")

        assert res.status_code == 400
        assert json.loads(res.data)["error"]

    def test_delete_alert_unauthenticated(self):
        """
        It should return an error 401 if the user is not logged in.
        """
        res = self.client.delete("/api/alert/{}".format(self.alert.sha))
        
        assert res.status_code == 401
        assert json.loads(res.data)["error"]

    def test_delete_alert(self):
        """
        It should delete an alert for the current user.
        """
        self.alert.save()

        with self.client.session_transaction() as session:
            res = self.client.post("/api/user/login", data=json.dumps({
                "email": self.user.email,
                "password": self.user.password
            }), content_type="application/json")
            res = self.client.delete("/api/alert/{}".format(self.alert.sha))

        assert res.status_code == 200
        assert json.loads(res.data)["success"]
        

    def test_get_user_alerts_unauthenticated(self):
        """
        It should return an error 401 if the user is not logged in.
        """
        res = self.client.get("/api/alert")

        assert res.status_code == 401
        assert json.loads(res.data)["error"]

    def test_get_user_alerts(self):
        """
        It should return all the current user's alerts.
        """
        self.alert.save()

        with self.client.session_transaction() as session:
            res = self.client.post("/api/user/login", data=json.dumps({
                "email": self.user.email,
                "password": self.user.password
            }), content_type="application/json")
            res = self.client.get("/api/alert")

        assert res.status_code == 200
        assert json.loads(res.data)["alerts"] == [self.alert.to_dict()]

class TestAlert(object):
    def setup(self):
        redis.flushdb()
        self.alert = Alert("user@host.ndd", "http://host.ndd/path")
        self.sha = sha1(self.alert.email).hexdigest()


    def test_save(self):
        """
        Alert.save should add the `alert_id` to 'alert:ids' and
        'account:{account_id}:alerts'.
        It should also save the attributes in 'alert:{alert_id}' as a dict.
        """
        self.alert.save()

        assert redis.sismember("sl:alert:ids", self.alert.sha) is True
        assert redis.sismember(
            "sl:account:{}:alerts".format(self.sha), self.alert.sha
        ) is True
        assert redis.hgetall(
            "sl:alert:{}".format(self.alert.sha)
        ) == self.alert.to_dict()

    def test_delete(self):
        """
        Alert.delete should remove the `alert_id` from 'alert:ids' and 
        'account:{account_id}:alerts'.
        """
        self.alert.save()
        Alert.delete(self.alert.sha)
        assert redis.sismember("sl:alert:ids", self.alert.sha) is False
        assert redis.sismember(
            "sl:account:{}:alerts".format(self.sha), 
            self.alert.sha
        ) is False

    def test_from_sha(self):
        """
        Alert.from_sha should return an Alert object.
        """
        self.alert.save()
        alert = Alert.from_sha(self.alert.sha)
        assert alert.to_dict() == self.alert.to_dict()

    def test_get_user_alerts(self):
        """
        Alert.get_user_alerts should return the `sha` of each alert
        associated to a given user.
        """
        als = [Alert("user@host.ndd", "http://host.ndd/path1"),
               Alert("user@host.ndd", "http://host.ndd/path2"),
               Alert("user@host.ndd", "http://host.ndd/path3")]

        map(Alert.save, als)

        assert Alert.get_user_alerts("user@host.ndd") == set([
            als[0].sha,
            als[1].sha,
            als[2].sha
        ])

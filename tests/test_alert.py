from app import redis, app, mode
from app.api import Alert, User
from flask import session, request
from mock import patch, MagicMock
from hashlib import sha1
app.testing = True

assert mode == "TEST"

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
        assert self.alert.save() is True

        assert redis.sismember("sl:alert:ids", self.alert.alert_sha) is True
        assert redis.sismember(
            "sl:account:{}:alerts".format(self.sha), self.alert.alert_sha
        ) is True
        assert redis.hgetall(
            "sl:alert:{}".format(self.alert.alert_sha)
        ) == self.alert.to_dict()

    def test_delete(self):
        """
        Alert.delete should remove the `alert_id` from 'alert:ids' and 
        'account:{account_id}:alerts'.
        """
        assert self.alert.save() is True
        assert Alert.delete(self.alert.alert_sha) is True
        assert redis.sismember("sl:alert:ids", self.alert.alert_sha) is False
        assert redis.sismember(
            "sl:account:{}:alerts".format(self.sha), 
            self.alert.alert_sha
        ) is False

    def test_from_sha(self):
        """
        Alert.from_sha should return an Alert object.
        """
        assert self.alert.save() is True
        alert = Alert.from_sha(self.alert.alert_sha)
        assert alert.to_dict() == self.alert.to_dict()

    def test_get_user_alerts(self):
        """
        Alert.get_user_alerts should return the `alert_sha` of each alert
        associated to a given user.
        """
        als = [Alert("user@host.ndd", "http://host.ndd/path1"),
               Alert("user@host.ndd", "http://host.ndd/path2"),
               Alert("user@host.ndd", "http://host.ndd/path3")]

        assert map(Alert.save, als) == [True, True, True]

        assert Alert.get_user_alerts("user@host.ndd") == set([
            als[0].alert_sha,
            als[1].alert_sha,
            als[2].alert_sha
        ])

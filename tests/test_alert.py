from app import redis, app
from flask import session, request
from mock import patch, MagicMock
from hashlib import sha1
import app.api.alert as alert
import app.api.user as user
rns = "test:"
alert.rns = rns
app.testing = True


class TestAlert(object):

    def clear_alert(self, al):
        email_sha = sha1(al.email).hexdigest()
        redis.srem(rns+"alert:ids", al.alert_sha)
        redis.srem(rns+"account:{}:alerts".format(email_sha), al.alert_sha)
        for key in al.to_dict():
            redis.hdel(rns+"alert:{}".format(al.alert_sha), key)

    def test_save(self):
        """
        Alert.save should add the `alert_id` to 'alert:ids' and
        'account:{account_id}:alerts'.
        It should also save the attributes in 'alert:{alert_id}' as a dict.
        """
        al = alert.Alert("user@host.ndd", "http://host.ndd/path")
        email_sha = sha1(al.email).hexdigest()

        self.clear_alert(al)
        assert al.save() is True

        assert redis.sismember(rns+"alert:ids", al.alert_sha) is True
        assert redis.sismember(rns+"account:{}:alerts".format(email_sha), al.alert_sha) is True
        assert redis.hgetall(rns+"alert:{}".format(al.alert_sha)) == al.to_dict()
        self.clear_alert(al)

    def test_delete(self):
        """
        Alert.delete should remove the `alert_id` from 'alert:ids' and 
        'account:{account_id}:alerts'.
        """
        al = alert.Alert("user@host.ndd", "http://host.ndd/path")
        email_sha = sha1(al.email).hexdigest()

        self.clear_alert(al)
        al.save()

        assert alert.Alert.delete(al.alert_sha) == True

        assert redis.sismember(rns+"alert:ids", al.alert_sha) is False
        assert redis.sismember(
            rns+"account:{}:alerts".format(email_sha), 
            al.alert_sha
        ) is False

        self.clear_alert(al)

    def test_from_sha(self):
        """
        Alert.from_sha should return an Alert object.
        """
        al = alert.Alert("user@host.ndd", "http://host.ndd/path")
        email_sha = sha1(al.email).hexdigest()

        self.clear_alert(al)
        al.save()

        assert alert.Alert.from_sha(al.alert_sha).to_dict() == al.to_dict()
        self.clear_alert(al)

    def test_get_user_alerts(self):
        """
        Alert.get_user_alerts should return the `alert_sha` of each alert
        associated to a given user.
        """
        als = [alert.Alert("user@host.ndd", "http://host.ndd/path1"),
               alert.Alert("user@host.ndd", "http://host.ndd/path2"),
               alert.Alert("user@host.ndd", "http://host.ndd/path3")]

        map(self.clear_alert, als)
        map(alert.Alert.save, als)

        assert alert.Alert.get_user_alerts("user@host.ndd") == set([als[0].alert_sha,
                                                                    als[1].alert_sha,
                                                                    als[2].alert_sha])
        map(self.clear_alert, als)

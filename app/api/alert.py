"""
Alert module

Contains the Alert class and the associated API endpoints.
"""
from app import app, redis
from hashlib import sha1
from flask import jsonify, make_response, request
from app.utils import is_authenticated


class Alert(object):
    """
    Alert class

    Represent an Alert with an email and an url.
    """
    def __init__(self, email, url, sha=None):
        """
        Return an alert from an email and an url.
        """
        self.email = email
        self.url = url
        self.sha = sha1(self.email + self.url).hexdigest() if not sha else sha

    def save(self):
        """
        Save the current alert to database.
        """
        email_sha = sha1(self.email).hexdigest()

        return bool(
            redis.sadd("sl:alert:ids", self.sha) and
            redis.sadd("sl:account:{}:alerts".format(email_sha), self.sha) and
            redis.hmset("sl:alert:{}".format(self.sha), self.to_dict())
        )

    @staticmethod
    def delete(alert_sha):
        """
        Delete the given alert.
        """
        alert = redis.hgetall("sl:alert:{}".format(alert_sha))
        sha = sha1(alert["email"]).hexdigest()

        return bool(
            alert and redis.srem("sl:alert:ids", alert_sha) and
            redis.srem("sl:account:{}:alerts".format(sha), alert_sha)
        )

    @classmethod
    def from_sha(cls, sha):
        """
        Return an Alert from a sha.
        """
        return cls(**redis.hgetall("sl:alert:{}".format(sha)))

    def to_dict(self):
        """
        Return a dict representation of the current alert.
        """
        return {
            "email": self.email,
            "url": self.url,
            "sha": self.sha
        }

    @staticmethod
    def get_user_alerts(email):
        """
        Return all the alerts associated with an email.
        """
        sha = sha1(email).hexdigest()

        return redis.smembers("sl:account:{}:alerts".format(sha))


@app.route('/api/alert', methods=['POST'])
@is_authenticated
def create_alert(user):
    """
    API endpoint creating an alert from an email and an url.
    """
    if not request.json:
        return make_response(jsonify({
            "error": "Could not create alert."
        }), 400)
    alert = Alert(request.json.get("email"), request.json.get("url"))
    user_alerts = Alert.get_user_alerts(user.email)
    if not user.plan or len(user_alerts) >= user.plan.alert_number:
        return make_response(jsonify({
            "error": "Too many alert already created."
        }), 400)
    elif alert.save():
        return make_response(jsonify(alert.to_dict()))
    else:
        return make_response(jsonify({
            "error": "Could not create alert."
        }), 400)


@app.route('/api/alert/<sha>', methods=['DELETE'])
@is_authenticated
def delete_alert(_, sha):
    """
    API endpoint deleting an alert from an email and an url.
    """
    if Alert.delete(sha):
        return make_response(jsonify({
            "success": "Alert has been removed successfully."
        }))
    else:
        return make_response(jsonify({
            "error": "Could not delete alert"
        }), 400)


@app.route('/api/alert')
@is_authenticated
def get_user_alerts(user):
    """
    API endpoint returning all the current user's alerts
    """
    alert_ids = list(Alert.get_user_alerts(user.email))
    if alert_ids is not None:
        alerts = [Alert.to_dict(alert) for alert in
                  [Alert.from_sha(sha) for sha in alert_ids]]
        return make_response(jsonify({"alerts": alerts}))
    else:
        return make_response(jsonify({
            "error": "Could not get user alerts"
        }), 400)

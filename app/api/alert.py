from app import app, redis
from hashlib import sha1
from flask import jsonify, make_response, abort, request
from app.utils import is_authenticated

class Alert(object):
    def __init__(self, email, url, sha=None):
        self.email = email
        self.url = url
        self.sha = sha1(self.email+self.url).hexdigest() if sha is None else sha

    def save(self):
        email_sha = sha1(self.email).hexdigest()

        return bool(
            redis.sadd("sl:alert:ids", self.sha) and
            redis.sadd("sl:account:{}:alerts".format(email_sha), self.sha) and
            redis.hmset("sl:alert:{}".format(self.sha), self.to_dict())
        )

    @staticmethod
    def delete(alert_sha):
        alert = redis.hgetall("sl:alert:{}".format(alert_sha))
        sha = sha1(alert["email"]).hexdigest()
    
        return bool(
            alert and redis.srem("sl:alert:ids", alert_sha) and
            redis.srem("sl:account:{}:alerts".format(sha), alert_sha)
        )

    @classmethod
    def from_sha(cls, sha):
        return cls(**redis.hgetall("sl:alert:{}".format(sha)))

    def to_dict(self):
        return {
            "email": self.email, 
            "url": self.url,
            "sha": self.sha
        }

    @staticmethod
    def get_user_alerts(email):
        sha = sha1(email).hexdigest()

        return redis.smembers("sl:account:{}:alerts".format(sha))

@app.route('/api/alert', methods=['POST'])
@is_authenticated
def create_alert(user):
    if not request.json:
        return make_response(jsonify({"error": "Could not create alert."}), 400)
    alert = Alert(request.json.get("email"), request.json.get("url"))

    if not user.plan or len(Alert.get_user_alerts(user.email)) >= user.plan.alert_number:
        return make_response(jsonify({"error": "Too many alert already created."}), 400)
    elif alert.save():
        return make_response(jsonify(alert.to_dict()))
    else:
        return make_response(jsonify({"error": "Could not create alert."}), 400)

@app.route('/api/alert/<sha>', methods=['DELETE'])
@is_authenticated
def delete_alert(user, sha):
    if Alert.delete(sha):
        return make_response(jsonify({"success": "Alert has been removed successfully."}))
    else:
        return make_response(jsonify({"error": "Could not delete alert"}), 400)

@app.route('/api/alert')
@is_authenticated
def get_user_alerts(user):
    alert_ids = list(Alert.get_user_alerts(user.email))
    if alert_ids is not None:
        alerts = map(Alert.to_dict, map(Alert.from_sha, alert_ids))
        return make_response(jsonify({"alerts": alerts}))
    else:
        return make_response(jsonify({"error": "Could not get user alerts"}), 400)

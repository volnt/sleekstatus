from app import app, redis
from hashlib import sha1
from flask import jsonify, make_response, abort, request
from user import is_authenticated

class Alert(object):
    def __init__(self, email, url):
        self.email = email
        self.url = url

    def save(self):
        alert_sha = sha1(self.email+self.url).hexdigest()
        email_sha = sha1(self.email).hexdigest()

        return (redis.sadd("sl:alert:ids", alert_sha) and
                redis.sadd("sl:account:{}:alerts".format(email_sha), alert_sha) and
                redis.hmset("sl:alert:{}".format(alert_sha), self.to_dict()))

    @staticmethod
    def delete(email, url):
        alert_sha = sha1(email+url).hexdigest()
        email_sha = sha1(email).hexdigest()

        alert = redis.hgetall("sl:alert:{}".format(alert_sha))
        return (alert and redis.srem("sl:alert:ids", alert_sha) and
                redis.srem("sl:account:{}:alerts".format(email_sha), alert_sha))
        

    @classmethod
    def from_sha(cls, sha):
        return cls(**redis.hgetall("sl:alert:{}".format(sha)))

    def to_dict(self):
        return {"email": self.email, "url": self.url }

    @staticmethod
    def get_user_alerts(email):
        sha = sha1(email).hexdigest()

        return redis.smembers("sl:account:{}:alerts".format(sha))

@app.route('/api/alert/create', methods=['POST'])
@is_authenticated
def create_alert():
    alert = Alert(request.json.get("email"), request.json.get("url"))

    if alert.save():
        return make_response(jsonify(alert.to_dict()))
    else:
        return make_response(jsonify({"error": "Could not create alert"}), 400)

@app.route('/api/alert/delete', methods=['POST'])
@is_authenticated
def delete_alert():
    if Alert.delete(request.json.get("email"), request.json.get("url")):
        return make_response(jsonify({"success": "Alert has been removed successfully."}))
    else:
        return make_response(jsonify({"error": "Could not create alert"}), 400)

@app.route('/api/alert')
@is_authenticated
def get_user_alerts(user):
    alert_ids = list(Alert.get_user_alerts(user.email))
    if alert_ids is not None:
        alerts = map(Alert.to_dict, map(Alert.from_sha, alert_ids))
        return make_response(jsonify({"alerts": alerts}))
    else:
        return make_response(jsonify({"error": "Could not get user alerts"}), 400)

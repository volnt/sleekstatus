from app import app
from flask import jsonify, make_response, abort, request
from app.utils import is_authenticated

class Plan(object):
    def __init__(self, _id, name, price, alert_number, interval="month", currency="usd"):
        self._id = _id
        self.name = name
        self.price = price
        self.interval = interval
        self.currency = currency
        self.alert_number = alert_number

    def subscribe(self, user):
        user.plan = self
        user.save()
        return True

    def unsubscribe(self, user):
        user.plan = None
        user.save()
        return True

    @classmethod
    def from_id(cls, _id):
        if _id in plans:
            return cls(**plans[_id])
        return None

    def to_dict(self):
        return {
            "id": self._id,
            "name": self.name,
            "price": self.price,
            "interval": self.interval,
            "currency": self.currency,
            "alert_number": self.alert_number
        }

@app.route('/api/plan/<_id>')
def plan_get(_id):
    plan = Plan.from_id(_id)

    if plan:
        return make_response(jsonify(plan.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Could not find plan '{}'"
                                      .format(_id)}))
    

@app.route('/api/plan/<_id>/subscribe', methods=['POST'])
@is_authenticated
def plan_subscribe(_id, user):
    if not request.json:
        return abort(400)
    plan = Plan.from_id(_id)

    if plan and plan.subscribe(user):
        return make_response(jsonify(plan.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Could not subscribe user."}), 400)
        

@app.route('/api/plan/<_id>/unsubscribe', methods=['POST'])
@is_authenticated
def plan_unsubscribe(_id, user):
    if not request.json:
        return abort(400)
    plan = Plan.from_id(_id)

    if plan and plan.unsubscribe(user):
        return make_response(jsonify({"success": "Unsubscribed user successfully."}), 200)
    else:
        return make_response(jsonify({"error": "Could not unsubscribe user."}), 400)
    
plans = {
    "basic": {
        "_id": "basic",
        "name": "Basic Plan",
        "price": "1.99",
        "interval": "month",
        "currency": "usd",
        "alert_number": 3,
    }, 
    "big": {
        "_id": "big",
        "name": "Big Plan",
        "price": "4.99",
        "interval": "month",
        "currency": "usd",
        "alert_number": 20,
    }, 
    "unlimited": {
        "_id": "unlimited",
        "name": "Unlimited Plan",
        "price": "19.99",
        "interval": "month",
        "currency": "usd",
        "alert_number": 1000,
    }
}

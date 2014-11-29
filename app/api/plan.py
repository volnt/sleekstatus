from app import app
from flask import jsonify, make_response, abort, request
from app.utils import is_authenticated

class Plan(object):
    def __init__(self, _id, name, amount, interval="month", currency="usd"):
        self._id = _id
        self.name = name
        self.amount = amount
        self.interval = interval
        self.currency = currency

    def subscribe(self, user):
        return True

    def unsubscribe(self, user):
        return True

    @classmethod
    def from_id(cls, _id):
        if _id in plans:
            return cls(**plans[_id])
        return None

    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "amount": self.amount,
            "interval": self.interval,
            "currency": self.currency
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
        return make_response(jsonify({"success": "Subscription success."}), 200)
    else:
        return make_response(jsonify({"error": "Could not subscribe user."}), 400)
        

@app.route('/api/plan/<_id>/unsubscribe', methods=['POST'])
@is_authenticated
def plan_unsubscribe(_id, user):
    if not request.json:
        return abort(400)
    plan = Plan.from_id(_id)

    if plan and plan.unsubscribe(user):
        return make_response(jsonify(plan.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Could not subscribe user."}), 400)
    
plans = {
    "basic": {
        "_id": "basic",
        "name": "Basic Plan",
        "amount": "1.99",
        "interval": "month",
        "currency": "usd"
    }, 
    "big": {
        "_id": "big",
        "name": "Big Plan",
        "amount": "4.99",
        "interval": "month",
        "currency": "usd"
    }, 
    "unlimited": {
        "_id": "unlimited",
        "name": "Unlimited Plan",
        "amount": "19.99",
        "interval": "month",
        "currency": "usd"
    }
}

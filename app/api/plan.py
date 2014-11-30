from app import app, stripe
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

    def subscribe(self, user, token):
        user.plan = self
        if not user.customer_token:
            try:
                customer = stripe.Customer.create(
                    card=token, 
                    plan=self._id, 
                    email=user.email
                )
            except Exception as e:
                print "Error : " + e
                return False
            else:
                user.customer_token = customer.id
                user.subscription_token = customer.subscriptions.data[0]["id"]
        else:
            customer = stripe.Customer.retrieve(user.customer_token)
            customer.card = token
            if user.subscription_token:
                subscription = customer.subscriptions.retrieve(
                    user.subscription_token
                )
                subscription.plan = self._id
                subscription.save()
            elif customer.subscriptions.total_count >= 1:
                subscription = customer.subscriptions.retrieve(
                    customer.subscriptions.data[0]["id"]
                )
                subscription.plan = self._id
                subscription.save()
            else:
                subscription = customer.subscriptions.create(plan=self._id)
        return user.save()

    def unsubscribe(self, user):
        customer = stripe.Customer.retrieve(user.customer_token) 
        user.subscription_token = customer.subscriptions.data[0]["id"]
        subscription = customer.subscriptions.retrieve(user.subscription_token).delete()
        user.plan = None
        return user.save()

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

@app.route('/api/plan/<_id>', methods=['POST'])
@is_authenticated
def plan_subscribe(_id, user):
    if not request.json:
        return abort(400)
    plan = Plan.from_id(_id)

    if plan and plan.subscribe(user, request.json.get("token")):
        return make_response(jsonify(plan.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Could not subscribe user."}), 400)
        

@app.route('/api/plan/<_id>', methods=['DELETE'])
@is_authenticated
def plan_unsubscribe(_id, user):
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

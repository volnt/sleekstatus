"""
Plan module

Contains the Plan class and the associated API endpoints.
"""
from app import app, stripe
from app import SleekException, catch_sleekexception
from flask import jsonify, make_response, abort, request
from app.utils import is_authenticated


class Plan(object):
    """
    Plan class

    Represent a plan with an _id, name, price, alert_number, interval and
    currency.
    """
    def __init__(self, _id, name, price, alert_number,
                 interval="month", currency="usd"):
        """
        Return a Plan
        """
        self._id = _id
        self.name = name
        self.price = price
        self.interval = interval
        self.currency = currency
        self.alert_number = alert_number

    def subscribe(self, user, token):
        """
        Subscribe given user to the current plan.

        The token is the card_token given by Stripe on client side.
        """
        user.plan = self
        if not user.customer_token:
            customer = stripe.Customer.create(
                card=token,
                plan=self._id,
                email=user.email
            )
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
                user.subscription_token = subscription.id
            elif customer.subscriptions.total_count >= 1:
                subscription = customer.subscriptions.retrieve(
                    customer.subscriptions.data[0]["id"]
                )
                subscription.plan = self._id
                subscription.save()
                user.subscription_token = subscription.id
            else:
                subscription = customer.subscriptions.create(plan=self._id)

        return user.save()

    @staticmethod
    def unsubscribe(user):
        """
        Unsubscribe a user from the current plan.
        """
        customer = stripe.Customer.retrieve(user.customer_token)
        user.subscription_token = customer.subscriptions.data[0]["id"]
        customer.subscriptions.retrieve(user.subscription_token).delete()
        user.plan = None

        return user.save()

    @classmethod
    def from_id(cls, _id):
        """
        Return a Plan based on a given `_id`.
        """
        if _id in PLANS:
            return cls(**PLANS[_id])
        return None

    def to_dict(self):
        """
        Return a dict representation of the current plan.
        """
        return {
            "id": self._id,
            "name": self.name,
            "price": self.price,
            "interval": self.interval,
            "currency": self.currency,
            "alert_number": self.alert_number
        }


@app.route('/api/plan/<_id>')
@catch_sleekexception
def plan_get(_id):
    """
    API endpoint returning the plan with the id `_id`.
    """
    plan = Plan.from_id(_id)

    if plan:
        return make_response(jsonify(plan.to_dict()), 200)
    else:
        raise SleekException("Could not find plan '{}'".format(_id), 404)

@app.route('/api/plan/<_id>', methods=['POST'])
@is_authenticated
@catch_sleekexception
def plan_subscribe(user, _id):
    """
    API endpoint subscribing the current user to the plan with the given _id.
    """
    if not request.json:
        raise SleekException("Could not subscribe user.")
    plan = Plan.from_id(_id)

    if plan and plan.subscribe(user, request.json.get("token")):
        return make_response(jsonify(plan.to_dict()), 200)
    else:
        raise SleekException("Could not subscribe user.")

@app.route('/api/plan/<_id>', methods=['DELETE'])
@is_authenticated
@catch_sleekexception
def plan_unsubscribe(user, _id):
    """
    API endpoint unsubscribing the current user from the plan wth the given
    _id.
    """
    plan = Plan.from_id(_id)

    if plan and plan.unsubscribe(user):
        return make_response(jsonify({
            "success": "Unsubscribed user successfully."
        }), 200)
    else:
        raise SleekException("Could not unsubscribe user.")

PLANS = {
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
        "name": "Huge Plan",
        "price": "19.99",
        "interval": "month",
        "currency": "usd",
        "alert_number": 1000,
    }
}

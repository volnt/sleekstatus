from app import redis, app, mode
from app.api import Alert, User, Plan
from flask import request
from mock import patch, MagicMock
from hashlib import sha1
import json
import stripe
app.testing = True

assert mode == "TEST"

class TestPlanAPI(object):
    def setup(self):
        redis.flushdb()
        self.user = User("user@host.ndd", "password")
        self.plan = Plan.from_id("basic")
        self.client = app.test_client()

    def test_plan_get(self):
        """
        It should get the plan with the corresponding `_id`.
        """
        for plan in ("basic", "big", "unlimited"):
            res = self.client.get("/api/plan/"+plan)

            assert res.status_code == 200
            assert json.loads(res.data)["id"] == plan

    @patch.object(Plan, "subscribe")
    def test_unauthenticated_plan_subscribe(self, subscribe):
        """
        It should return an 401 error because this endpoint needs 
        authentication.
        """
        res = self.client.post("/api/plan/basic", data=json.dumps({
            "token": "randomtoken"
        }), content_type="application/json")

        assert res.status_code == 401
        assert json.loads(res.data)["error"]
        assert subscribe.called is False

    @patch.object(Plan, "subscribe")
    def test_plan_subscribe(self, subscribe):
        """
        It should subscribe the authenticated user to the corresponding plan.
        """
        with self.client.session_transaction() as session:
            res = self.client.post("/api/user/login", data=json.dumps({
                "email": self.user.email,
                "password": self.user.password
            }), content_type="application/json")
            res = self.client.post("/api/plan/basic", data=json.dumps({
                "token": "randomtoken"
            }), content_type="application/json")

        assert res.status_code == 200
        assert json.loads(res.data)["id"] == "basic"
        subscribe.assert_called_once()

    @patch.object(Plan, "unsubscribe")
    def test_unauthenticated_plan_unsubscribe(self, unsubscribe):
        """
        It should return an 401 error because this endpoint needs 
        authentication.
        """
        res = self.client.delete("/api/plan/basic")

        assert res.status_code == 401
        assert json.loads(res.data)["error"]
        assert unsubscribe.called is False

    @patch.object(Plan, "unsubscribe")
    def test_plan_unsubscribe(self, unsubscribe):
        """
        It should unsubscribe the authenticated user from the corresponding 
        plan.
        """
        with self.client.session_transaction() as session:
            res = self.client.post("/api/user/login", data=json.dumps({
                "email": self.user.email,
                "password": self.user.password
            }), content_type="application/json")
            res = self.client.delete("/api/plan/basic")

        assert res.status_code == 200
        assert json.loads(res.data)["success"]
        unsubscribe.assert_called_once()


class TestPlan(object):
    def setup(self):
        redis.flushdb()
        self.plan = Plan.from_id("basic")
        self.user = User("user@host.ndd", "password")
        self.token = stripe.Token.create(card={
            "number": '4242424242424242',
            "exp_month": 12,
            "exp_year": 2015,
            "cvc": '123'
        })

    def test_new_customer_subscribe(self):
        """
        It should create a customer and subscribe it to the current plan if 
        the user is not yet a customer.
        """

        assert self.plan.subscribe(self.user, self.token)  is True
        assert self.user.customer_token is not None
        assert self.user.subscription_token is not None
        customer = stripe.Customer.retrieve(self.user.customer_token)
        subscription = customer.subscriptions.retrieve(
            self.user.subscription_token
        )
        assert subscription.plan["id"] == self.plan._id
        assert customer.delete()["deleted"] is True

    def test_customer_subscribe(self):
        """
        It should update the plan of the current user to the current plan if
        the customer has already subscribed to a plan.
        """
        customer = stripe.Customer.create(
            card=self.token,
            plan="big",
            email=self.user.email
        )
        self.user.customer_token = customer.id

        assert customer.subscriptions.total_count == 1
        assert self.plan.subscribe(self.user, self.token) is True
        assert self.user.subscription_token is not None
        customer = stripe.Customer.retrieve(customer.id)
        assert customer.subscriptions.total_count == 1
        subscription = customer.subscriptions.retrieve(
            self.user.subscription_token
        )
        assert subscription.plan["id"] == self.plan._id
        assert customer.delete()["deleted"] is True

    def test_customer_no_plan_subscribe(self):
        """
        It should set the current user's plan to the current plan if the
        customer has not yet subscribed to a plan.
        """
        customer = stripe.Customer.create(
            card=self.token,
            email=self.user.email
        )
        self.user.customer_token = customer.id

        assert customer.subscriptions.total_count == 0
        assert self.plan.subscribe(self.user, self.token) is True
        customer = stripe.Customer.retrieve(customer.id)
        assert customer.subscriptions.total_count == 1
        assert customer.delete()["deleted"] is True

    def test_unsubscribe(self):
        """
        It should unsubscribe the given user from its plan.
        """
        customer = stripe.Customer.create(
            card=self.token,
            plan=self.plan._id,
            email=self.user.email
        )
        self.user.customer_token = customer.id

        assert customer.subscriptions.total_count == 1
        assert Plan.unsubscribe(self.user) is True
        customer = stripe.Customer.retrieve(customer.id)
        assert customer.subscriptions.total_count == 0
        assert customer.delete()["deleted"] is True

    def test_from_id(self):
        """
        It should return the plan corresponding to the given `_id`.
        """
        assert Plan.from_id("basic")._id == "basic"
        assert Plan.from_id("big")._id == "big"
        assert Plan.from_id("unlimited")._id == "unlimited"

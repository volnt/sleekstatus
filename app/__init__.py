"""
Sleekstatus module
"""
from app.sleekexception import SleekException, catch_sleekexception
from flask import Flask
import redis
import os
import stripe
import sys

app = Flask(__name__)
app.secret_key = os.urandom(32)

if "py.test" in sys.argv[0]:
    redis = redis.Redis(db=2)
    mode = "TEST"
else:
    redis = redis.Redis()
    mode = "PROD"

stripe.api_key = "sk_test_Btmp0w2nKxakPnstPjToGwgP"

from app.api import alert, user, plan
from app import views

__all__ = ["user", "alert", "plan", "views",
           "SleekException", "catch_sleekexception"]

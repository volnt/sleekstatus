"""
Sleekstatus module
"""
from app.sleekexception import SleekException, catch_sleekexception
from flask import Flask
import redis
from celery import Celery
import os
import stripe
import sys

app = Flask(__name__)
app.secret_key = os.urandom(32)

async = Celery('sl', broker='amqp://localhost')

if "py.test" in sys.argv[0] or "--test" in sys.argv:
    redis = redis.Redis(db=2)
    mode = "TEST"
else:
    redis = redis.Redis(
        host="wh-redis.db18vl.ng.0001.usw2.cache.amazonaws.com",
        port=6379
    )
    mode = "PROD"

stripe.api_key = "sk_test_Btmp0w2nKxakPnstPjToGwgP"

from app.api import alert, user, plan
from app import views

__all__ = ["user", "alert", "plan", "views",
           "SleekException", "catch_sleekexception"]

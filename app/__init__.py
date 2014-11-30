from flask import Flask
import redis
import os
import stripe

app = Flask(__name__)
app.secret_key = os.urandom(32)

redis = redis.Redis()
rns = "sl:" # redis namespace

stripe.api_key = "sk_test_Btmp0w2nKxakPnstPjToGwgP"

from app.api import alert, user, plan
from app.views import index

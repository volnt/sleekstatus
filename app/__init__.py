from flask import Flask
import redis
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

redis = redis.Redis()

from app.api import alert, user, plan
from app.views import index

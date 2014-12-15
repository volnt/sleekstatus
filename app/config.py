"""
Config module

Contains the MAIL object containing the different informations
needed to connect to the smtp server.
"""
from os import environ

AWS = {
    "ACCESS_KEY_ID": environ["AWS_ACCESS_KEY_ID"],
    "SECRET_ACCESS_KEY": environ["AWS_SECRET_ACCESS_KEY"]
}

"""
Config module

Contains the MAIL object containing the different informations
needed to connect to the smtp server.
"""
from os import environ

MAIL = {
    "LOGIN": environ["MAIL_LOGIN"],
    "PASSWORD": environ["MAIL_PASSWORD"],
    "ADDR": environ["MAIL_ADDR"],
    "SMTP": environ["MAIL_SMTP"]
}

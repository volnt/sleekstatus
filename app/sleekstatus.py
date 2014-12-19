"""
Sleekstatus module

It processes the alerts stored in database when called.
"""
from app.utils import send_email
from app import redis
import requests


def get_alert_ids():
    """
    Fetch alert ids from database.
    """
    return redis.smembers("sl:alert:ids")


def get_alert(alert_id):
    """
    Fetch a given alert informations from database.
    """
    return redis.hgetall("sl:alert:{}".format(alert_id))


def trigger_alert(alert):
    """
    Sends a given alert by mail.
    """
    subject = "[WEBSTATUS] {} - KO".format(alert["url"])
    content = """Hi, it seems that your website is down."""
    send_email.delay("trash@volent.fr", subject, content, [alert["email"]])


def main():
    """
    Triggers alerts when requests.get(alert["url"]) fails.
    """
    slids = get_alert_ids()
    for slid in slids:
        alert = get_alert(slid)
        print alert
        if not requests.get(alert["url"]).ok:
            trigger_alert(alert)

if __name__ == "__main__":
    main()

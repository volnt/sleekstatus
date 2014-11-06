from app.utils import Mail
from app import redis
import requests

def get_alert_ids():
    return redis.smembers("sl:alert:ids")

def get_alert(alert_id):
    return redis.hgetall("sl:alert:{}".format(alert_id))

def trigger_alert(alert):
    subject = "[WEBSTATUS] {} - KO".format(alert["url"])
    content = """Hi, it seems that your website is down."""
    Mail(subject, content, [alert["email"]]).send()

def main():
    slids = get_alert_ids()
    for slid in slids:
        alert = get_alert(slid)
        print alert
        if not requests.get(alert["url"]).ok:
            trigger_alert(alert)

if __name__ == "__main__":
    main()

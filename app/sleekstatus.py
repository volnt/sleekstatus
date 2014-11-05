from ast import literal_eval
from app.utils import Mail
import requests
import redis

redis = redis.Redis()

def main():
    ids = redis.smembers("webstatus:ids")
    for wid in ids:
        status = literal_eval(redis.get("webstatus:{}".format(wid)))
        if not requests.get(status["url"]).ok:
            subject = "[WEBSTATUS] {} - KO".format(status["url"])
            content = """Hi, it seems that your website is down."""
            Mail(subject, content, [status["email"]]).send()

if __name__ == "__main__":
    main()

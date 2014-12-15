"""
Mail module

Contains the Mail class that's used to send mails.
"""
from app import async
from app.config import AWS
import boto.ses

@async.task
def send_email(from_addr, subject, body, to_addr_list):
    conn = boto.ses.connect_to_region(
        'us-west-2',
        aws_access_key_id=AWS["ACCESS_KEY_ID"],
        aws_secret_access_key=AWS["SECRET_ACCESS_KEY"]
    )
    return conn.send_email(from_addr, subject, body, to_addr_list)

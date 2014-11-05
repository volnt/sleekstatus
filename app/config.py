from os import environ

MAIL = {
    "LOGIN": environ["MAIL_LOGIN"],
    "PASSWORD": environ["MAIL_PASSWORD"],
    "ADDR": environ["MAIL_ADDR"],
    "SMTP": environ["MAIL_SMTP"]
}


"""
Mail module

Contains the Mail class that's used to send mails.
"""
from app.config import MAIL
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import smtplib
import os


class Mail(object):
    """
    Example :

    >>> Mail("foo", "bar").send()
    """
    def __init__(self, subject, message, to_addr_list, files):
        """
        Args:
            subject (str): the mail subject
            message (str): the mail content
            to_addr_list (list): the list of the recipients
            files (list): a list of attached files
        """
        self.to_addr_list = to_addr_list
        self.cc_addr_list = []
        self.files = files
        self.subject = subject
        self.message = message

    def build_msg(self):
        """
        Build and return the MIMEMultipart object.
        """
        msg = MIMEMultipart()
        msg['From'] = MAIL["ADDR"]
        msg['To'] = ", ".join(self.to_addr_list)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.message))

        for attachment in self.files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachment, "rb").read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment; filename="%s"' % os.path.basename(attachment)
            )
            msg.attach(part)

        return msg

    def send(self):
        """
        Sends the mail we created

        >>> Mail("subject", "mail content").send()
        """
        msg = self.build_msg()

        smtp = smtplib.SMTP(MAIL["SMTP"])
        smtp.starttls()
        smtp.login(MAIL["LOGIN"], MAIL["PASSWORD"])
        smtp.sendmail(MAIL["ADDR"], self.to_addr_list, msg.as_string())
        smtp.close()

from app.config import MAIL
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import smtplib
import os
import sys


class Mail(object):
    """
    Example :

    >>> Mail("foo", "bar").send()
    """
    def __init__(self, subject, message, to_addr_list, files=[]):
        """
        Args:
            subject (str): the mail subject
            message (str): the mail content
            to_addr_list (list): the list of the recipients
            files (list): a list of attached files
        """
        self.login = MAIL["LOGIN"]
        self.password = MAIL["PASSWORD"]
        self.from_addr = MAIL["ADDR"]
        self.to_addr_list = to_addr_list
        self.cc_addr_list = []
        self.files = files
        self.subject = subject
        self.message = message
        self.smtp = MAIL["SMTP"]

    def send(self):
        """
        Sends the mail we created

        >>> Mail("subject", "mail content").send()
        """

        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = COMMASPACE.join(self.to_addr_list)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.message))

        for f in self.files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            Encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment; filename="%s"' % os.path.basename(f)
            )
            msg.attach(part)

        smtp = smtplib.SMTP(self.smtp)
        smtp.starttls()
        smtp.login(self.login, self.password)
        try:
            smtp.sendmail(self.from_addr, self.to_addr_list, msg.as_string())
        except Exception as e:
            sys.stdout.write(e)
        smtp.close()

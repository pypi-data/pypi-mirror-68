#!/usr/bin/env python

from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
UTF8="utf-8"


def _format_addr(name, addr):
    if not isinstance(name, bytes):
        name = name.encode(UTF8, 'ignore')
    return formataddr(
        (
            Header(name, UTF8).encode(),
            addr
        )
    )

class Sendmail:
    def __call__(self,to_addr, *args,**kwds):
        if isinstance(to_addr,(list,tuple)):
            for i in to_addr:
                self.send(i,*args,**kwds)
        else:
            self.send(to_addr, *args, **kwds)


    def send(self, to_addr, title, txt, to_name=None, from_addr=None, name=None, html=None):
        if name is None:
            name = self.name
        if from_addr is None:
            from_addr = self.mail

        if to_name is None:
            to_name = to_addr.split("@", 1)[0]

        msg = MIMEMultipart('alternative')
        if txt:
            msg.attach( MIMEText(txt, 'plain', UTF8) )
        if html:
            msg.attach( MIMEText(html, 'html', UTF8) )

        msg['From'] = _format_addr(name, from_addr)
        msg['To'] = _format_addr(to_name, to_addr)
        msg['Subject'] = Header(title, UTF8).encode()
        msg.add_header('Reply-to', self.reply_to)
        msg = msg.as_string()

        port = self.smtp_port
        if port == 465:
            smtp = smtplib.SMTP_SSL(self.smtp_host, port)
        else:
            smtp = smtplib.SMTP(self.smtp_host, port)

        #smtp.set_debuglevel(1)

        smtp.ehlo()
        if port != 25 and port!=465:
            smtp.starttls()
            smtp.ehlo()
        smtp.login(self.smtp_user, self.smtp_password)
        addr_li = [to_addr]
        if self.backup:
            addr_li.append(self.backup)
        smtp.sendmail(from_addr, addr_li, msg)
        smtp.quit()

    def __init__(self, name, mail, reply_to, smtp_host, smtp_port, smtp_user, smtp_password, backup=None):
        self.name = name
        self.mail = mail
        self.reply_to = reply_to
        self.backup = backup
        self.smtp_host=smtp_host
        self.smtp_port=smtp_port
        self.smtp_user=smtp_user
        self.smtp_password=smtp_password

if __name__ == "__main__":
    from datetime import datetime
    mail_li = [
        "xpure@foxmail.com",
    ]
    from config import CONFIG
    sendmail = Sendmail(**CONFIG)
    for mail in mail_li:
        title = f"测试 {mail} {datetime.now()}"
        txt = f"""{title}
{__file__}
"""
        #sendmail([mail], title, txt)
        sendmail(mail, title, txt)

#!/usr/bin/env python3
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from common.base import Singleton


def pul_log_message(pul_log):
    e_message = "Total: {0} \r\n " \
                "Delivered: {1} \r\n " \
                "Revision Duplicated: {2} \r\n " \
                "Revision Changed: {3} \r\n " \
                "Fresh Items: {4} \r\n " \
                "Job Time: {5} \r\n "
    return e_message.format(pul_log.total,
                            pul_log.delivered,
                            pul_log.revision_duplicated,
                            pul_log.revision_changed,
                            pul_log.fresh_item,
                            pul_log.trans_time)


def build_message(_from, _to, _cc, _bcc, subject, content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = Header(_from)
    message['To'] = Header(','.join(_to))
    message['CC'] = Header(','.join(_cc))
    message['BCC'] = Header(','.join(_bcc))
    print(message)
    return message


class MailUtil(Singleton):

    def __init__(self):
        super(MailUtil, self).__init__()
        self._host = self.config.get('email', 'host')
        self._port = self.config.get('email', 'port')
        self._user_name = self.config.get('email', 'user_name')
        self._password = self.config.get('email', 'password')
        self._sender = self.config.get('email', 'sender')
        self._receivers = self.config.get('email', 'receivers')
        self._receivers = self._receivers.split(',')

    def init_smpt(self):
        smtp = smtplib.SMTP(host=self._host, port=self._port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self._user_name, self._password)
        return smtp

    def send_pul_log(self, pul_log):
        cc = [self._sender]
        to = self._receivers + cc
        content = pul_log_message(pul_log)
        subject = "{0}, PUL Monitor Notification" % pul_log.trans_time
        message = build_message(self._sender, to, cc, [], subject, content)
        smtp = self.init_smpt()
        smtp.sendmail(self._sender, to, message.as_string())
        smtp.close()

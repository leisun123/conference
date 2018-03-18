#coding:utf-8
"""
@file:      mail
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    05/03/2018 1:03 AM
@description:
            --
"""

import os

import django
SETTINGS = 'conference.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS
django.setup()
from django.template.loader import get_template
from django.template import loader
from conference import settings

from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
from conference import settings



class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)

def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()
    
#send_mail("123", "123", settings.DEFAULT_FROM_EMAIL, recipient_list=['genius_wz@aliyun.com',], html='core/base.html')

data = {'scholarname':'wang'}

email_content = get_template('share_layout/email.html').render(data)
send_mail("123", "123", settings.DEFAULT_FROM_EMAIL, recipient_list=['genius_wz@aliyun.com',], html=email_content)


















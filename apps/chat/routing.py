#coding:utf-8
"""
@file:      routing
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    14/03/2018 11:07 PM
@description:
            --
"""
from django.conf.urls import url
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<slug:room_name>/', consumers.ChatConsumer),
]


#coding:utf-8
"""
@file:      urls
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    14/03/2018 10:25 PM
@description:
            --
"""

from django.urls import path

from apps.chat import views

urlpatterns = [
    path('chat/', views.index, name='chatindex'),
    path('chat/<slug:room_name>/', views.room, name='room'),
]
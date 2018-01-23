#coding:utf-8
"""
@file:      urls
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/1/23 上午12:41
@description:
            --
"""
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^password/$', views.password, name='password'),
    url(r'updateimage/$', views.updateImage, name='updateimage'),
]
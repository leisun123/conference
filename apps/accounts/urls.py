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
from django.urls import path

from . import views

urlpatterns = [
    path(r'login/', views.login, name='login'),
    path(r'logout/', views.logout, name='logout'),
    path(r'register/', views.register, name='register'),
    path(r'password/', views.password, name='password'),
    path(r'updateimage/', views.updateImage, name='updateimage'),
]
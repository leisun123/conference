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
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('changepasswd/', views.password, name='change_password'),
    path('password/', views.password, name='password'),
    path('updateimage/', views.updateImage, name='updateimage'),
]
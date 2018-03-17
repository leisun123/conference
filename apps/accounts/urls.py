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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('password/', views.password, name='password'),
    path('updateimage/', views.updateImage, name='updateimage'),
    path("accounts/password_change/", auth_views.password_change, name='password_change'),
    path("accounts/password_change/done/", auth_views.password_change_done, name='password_change_donw'),
    path("accounts/password_reset/", auth_views.password_reset, name="password_reset"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.password_reset_confirm, name='password_reset_confirm'),
    path("accounts/reset/done/", auth_views.password_reset_complete, name='password_reset_complete'),
]
#coding:utf-8
"""
@file:      urls
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/1/22 下午2:51
@description:
            --
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('content/<int:content_id>',
        views.GenericTabContentView.as_view(),
        name='genericTagContentById'),
    path('showscholar/', views.ScholarListView.as_view(), name='scholarList'),
    
]

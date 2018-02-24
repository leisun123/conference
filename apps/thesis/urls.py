#coding:utf-8
"""
@file:      urls
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/2/5 下午8:17
@description:
            --
"""
from django.conf.urls import url
from apps.thesis.views import UploadView, ReviewIndexView, ReviewView, EditorReviewView

urlpatterns = [
    url(r'upload/$', UploadView.as_view(), name='upload'),
    url(r'reviewIndex/$', ReviewIndexView.as_view(), name='reviewIndex'),
    url(r'^review/(?P<thesis_id>\d+)$', ReviewView.as_view(),
        name='thesisReviewById'),
    url(r'^editor/(?P<thesis_id>\d+)$', EditorReviewView.as_view(),
        name='editorReviewById')
]
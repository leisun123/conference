#coding:utf-8
"""
@file:      urls
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    02/03/2018 10:42 AM
@description:
            --
"""
from django.urls import path

from apps.PaperReview import views

urlpatterns = [
    path('listpaper', views.PaperListView.as_view(), name='list_paper'),
    path('createpaper/', views.PaperCreateView.as_view(), name='create_paper'),
    path('displaypaper/<int:pk>', views.PaperDisplayView.as_view(), name='display_paper'),
    path('updatepaper/<int:pk>', views.PaperUpdateView.as_view(), name='update_paper'),
    
    path('listassignment', views.AssignmentListView.as_view(), name='list_assignment'),
    path('createassigenment/<int:pk>', views.AssignmentCreateView.as_view(), name='create_assignment'),
    path('displayassignment/<int:pk>', views.AssignmentDisplayView.as_view(), name='display_assignment'),
    
    path('createreview/<int:pk>', views.ReviewCreateView.as_view(), name='create_review'),
    path('displayreview/<int:pk>', views.ReviewDisplayView.as_view(), name='display_review'),
    path('status', views.StatusView.as_view(), name='status'),
]

#coding:utf-8
"""
@file:      mixins
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    27/02/2018 3:05 PM
@description:
            --
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render

from apps.PaperReview.models import Paper, Assignment, Review
from apps.accounts.models import Scholar
from django.contrib.contenttypes.models import ContentType

class AccessDeniedMixin(LoginRequiredMixin, object):
    

    def check(self, request, **kwargs):
        
        user = request.user
        
        groups = list(user.groups.all())
        
        view = self.__class__.__name__.lower()
        
        if self.request.user.is_superuser:
            return
        
        def check_access_view():
            if "paper" in view:
                return Paper.objects.filter(uploader__groups__in=groups).count() == 0
            elif "assign" in view:
                return Assignment.objects.filter(editor__groups__in=groups).count() == 0
            elif "review" in view:
                return Review.objects.filter(reviewer__groups__in=groups).count() == 0
        
        return render(request, 'share_layout/403.html') if check_access_view() else None
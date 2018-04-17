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
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


class AccessDeniedMixin(LoginRequiredMixin, object):
    
    def check(self, request, **kwargs):
        
        user = request.user
        groups = [group.name for group in user.groups.all()]
        view = self.__class__.__name__.lower()
        
        if self.request.user.is_superuser:
            return
        
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(
                reverse('login')
            )
        
        def check_access_view():
    
            if "paper" in view:
                return "scholar" not in groups
            elif "assign" in view:
                return "editor" not in groups
            elif "review" in view:
                return "reviewer" not in groups
        
        return render(request, 'share_layout/403.html') if check_access_view() else None
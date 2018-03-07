#coding:utf-8
"""
@file:      main_tags
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/1/22 下午3:00
@description:
            --
"""
import os
from django import template

from itertools import zip_longest

from django.urls import reverse

from apps.PaperReview.models import Paper

register = template.Library()

@register.simple_tag
def query(qs, count=False, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    if count is True:
        return qs.filter(**kwargs).count()
    return qs.filter(**kwargs)

@register.simple_tag
def filename(fname):
    return os.path.basename(fname)
    
@register.inclusion_tag('main/tags/scholar_particular_info.html')
def load_scholar_info(scholar, user=None):
    
    return {
        'id': scholar.id,
        'avatar': scholar.avatar.name,
        'current_user': user.username if user else "",
        'username': scholar.username,
        'organization': scholar.organization,
        'email': scholar.email,
        'keywords': scholar.keywords.split[','] if isinstance(scholar.keywords, list) else [],
        'thesis_set': list(zip_longest(scholar.thesis_author.all(), scholar.review_set.all(), fillvalue=""))
    }
@register.inclusion_tag('main/tags/scholar_list_info.html')
def load_scholar_list_info(scholar):
    return {
        'id': scholar.id,
        'scholar': scholar,
        'avatar': scholar.avatar,
        'username': scholar.username,
        'organization': scholar.organization,
        'major': scholar.major,
        'keywords': scholar.keywords.split(',') if isinstance(scholar.keywords, list) else [],
    }

    


    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
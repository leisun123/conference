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

from django.contrib.auth.models import Permission
from django.urls import reverse
from guardian.models import UserObjectPermission

from apps.PaperReview.models import Paper
from conference import settings

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

@register.simple_tag
def load_file(filefield):
    return os.path.join(settings.MEDIA_URL, filefield)

@register.simple_tag
def load_permission_paper(request):
    
        content_type = Permission.objects.get(codename='view_paper').content_type
        
        return \
            [Paper.objects.get(id=obj.object_pk) for obj in UserObjectPermission.objects\
            .filter(user=request.user, content_type=content_type).all()]

    
@register.inclusion_tag('Judgment/sidebar.html')
def load_judgment_sidebar(sidebar_type):
    dic = {
        "paper": [{"overview": "list_paper"},
                  {"upload": "create_paper"},
                  {"status": "status"}],
        #TODO: waiting assign
        "assignment": [{"overview": "list_assignment"},
                       ],
        #TODO: overview
        "review": [{"review": "create_review"}]
    }
    return dic.get(sidebar_type)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
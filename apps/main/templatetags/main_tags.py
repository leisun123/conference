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

from apps.PaperReview.models import Paper, Assignment
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
    
@register.inclusion_tag('main/scholar_list_info.html')
def load_scholar_list_info(scholar):
    return {
        'id': scholar.id,
        'scholar': scholar,
        'name': scholar.name,
        'organization': scholar.organization,
        'editor_proposal': scholar.paper.assignment.proposal_to_author,
    }

@register.inclusion_tag('main/scholar_particular_info.html')
def load_scholar_detail_info(scholar):
    
    return {
        'id': scholar.id,
        'name': scholar.name,
        'organization': scholar.organization,
        'email': scholar.email,

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
        "paper": [["overview", "list_paper"],
                  ["upload", "create_paper"],
                  ["status", "status"]],
        
        "assignment": [["overview", "list_assignment"],
                       ],
        
        "review": [["overview", "list_review"]]
    }
    return {'sidebarnode_list': dic.get(sidebar_type)}
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
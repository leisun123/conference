#coding:utf-8
"""
@file:      context_processors
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/1/21 下午4:40
@description:
            --
"""
from .models import SideBar, GenericTagContent
from apps.PaperReview.models import Paper

def sidebar_processor(requests):
    value = {
        'sidebar_node_list': SideBar.objects.all(),
    }
    return  value


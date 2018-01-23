#coding:utf-8
"""
@file:      adminx
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/1/22 下午4:15
@description:
            --
"""

import xadmin

from .models import SideBar, GenericTagContent


class GenericTagContentAdmin(object):
    list_display = ['theme', 'status', 'created_time', 'last_mod_time', 'sidebar']
    search_fields = ['theme', 'body']
    list_filter = ['sidebar__node_name']
    style_fields = {'body': 'ueditor'}
    relfield_style = 'fk-ajax'

class SideBarAdmin(object):
    list_display = ['node_name', 'rank', 'created_time', 'last_mod_time', 'parent_node']
    search_fields = ['node_name']
    
xadmin.site.register(SideBar, SideBarAdmin)
xadmin.site.register(GenericTagContent, GenericTagContentAdmin)
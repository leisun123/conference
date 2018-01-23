#coding:utf-8
"""
@file:      adminx
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/1/22 下午11:46
@description:
            --
"""
#coding:utf8

__author__ = 'liuhui'

import xadmin
from xadmin import views




class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "会议后台管理"
    site_footer = "江苏省教育大数据重点实验室  © copyright wyn"
    menu_style = 'accordion'

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)



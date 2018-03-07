#coding:utf-8
"""
@file:      urls
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/1/22 下午2:51
@description:
            --
"""
from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path('content/<int:content_id>',
        views.GenericTabContentView.as_view(),
        name='genericTagContentById'),
    path('scholarShow/', views.ScholarListView.as_view(), name='scholarList'),
    
]

# 'example.views',
#     url(r'^stacked/$', 'formset', {'formset_class': ContactFormset, 'template': 'example/formset-stacked.html'}, name='example_stacked'),
#     url(r'^table/$', 'formset', {'formset_class': ContactFormset, 'template': 'example/formset-table.html'}, name='example_table'),
#     url(r'^form-template/$', 'formset_with_template', {'formset_class': EmptyContactFormset, 'template': 'example/form-template.html'}, name='example_form_template'),
#     url(r'^admin-widget/$', 'formset', {'formset_class': EventFormset, 'template': 'example/formset-admin-widget.html'}, name='example_admin_widget'),
#     url(r'^multiple-formsets/$', 'multiple_formsets', {'template': 'example/formset-multiple-formsets.html'}, name='example_multiple_formsets'),
#     url(r'^inline-formset/$', 'inline_formset',
#        {'form_class': OrderedItemForm, 'template': 'example/inline-formset.html'}, name='example_inline_formset'),
#     url(r'^inline-formset-autocomplete/$', 'inline_formset',
#        {'form_class': AutoCompleteOrderedItemForm, 'template': 'example/inline-formset-autocomplete.html'}, name='example_inline_autocomplete'),
#     url(r'^inline-formset-ajax-selects/$', 'inline_formset',
#        {'form_class': AutoCompleteSelectFieldForm, 'template': 'example/inline-formset-django-ajax-select.html'}, name='example_inline_ajax_selects'),
#     url(r'^autocomplete-products/$', 'autocomplete_products', name='example_autocomplete_products')
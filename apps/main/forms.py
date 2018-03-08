# #coding:utf-8
# """
# @file:      forms
# @author:    IsolationWyn
# @contact:   genius_wz@aliyun.com
# @python:    3.5.2
# @editor:    PyCharm
# @create:    01/03/2018 10:54 AM
# @description:
#             --
# """
#
# from django import forms
# from django.contrib.admin.widgets import AdminDateWidget
# from django.forms import fields, formsets, widgets
#
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout
# from conference import settings
#
#
# class EventForm(forms.Form):
#     name = fields.CharField(max_length=150, label='display name')
#
#
#
#
# EventFormset = formsets.formset_factory(EventForm, extra=1)
#
#
# CONTACT_INFO_TYPES = (
#     ('Phone', 'Phone'),
#     ('Fax', 'Fax'),
#     ('Email', 'Email'),
#     ('AIM', 'AIM'),
#     ('Gtalk', 'Gtalk/Jabber'),
#     ('Yahoo', 'Yahoo'),
# )
#
#
#
#
# class ContactInfoForm(forms.Form):
#     type = fields.ChoiceField(choices=CONTACT_INFO_TYPES)
#     value = fields.CharField(max_length=200)
#     preferred = fields.BooleanField(required=False)
#
#
#
#
# ContactFormset = formsets.formset_factory(ContactInfoForm, extra=1)
#
# class ExampleFormSetHelper(FormHelper):
#     def __init__(self, layout, *args, **kwargs):
#         super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
#         self.form_method = 'post'
#         self.layout = layout
#
#         self.template = 'bootstrap3/my_table_formset.html'
#         self.render_required_fields = True
#
# helper = ExampleFormSetHelper(layout=Layout(
#             'name'
#         ))
#
#

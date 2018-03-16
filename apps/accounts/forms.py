#coding:utf-8
"""
@file:      form
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/1/22 下午11:49
@description:
            --
"""
#coding:utf8
import random

from django import forms
from django.contrib import auth

from apps import PaperReview
from apps.PaperReview.models import Paper
from apps.accounts.models import Scholar
from guardian.shortcuts import assign_perm
from django.utils import timezone

class LoginForm(forms.ModelForm):

    class Meta:
        model = Scholar
        fields = ('email', 'password',)

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = auth.authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('email or password invalid')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('error, connect administrator(isolationwyn@gmail.com)')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = Scholar
        fields = ('username', 'organization', 'email',
                  'keywords', 'major')

    def __init__(self, *args, **kwargs):
        self.user = None
        super(RegisterForm, self).__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Scholar.objects.get(email=email)
            raise forms.ValidationError(u'该邮箱已被注册')
        except Scholar.DoesNotExist:
            return email

    def clean_res_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('res_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'两次输入密码不一致')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class PasswordChangeForm(forms.Form):

    class Meta:
        model = Scholar
        fields = ['old_password', 'password', 'res_password',]

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        res_password = self.cleaned_data.get("res_password")
        if password and res_password and password != res_password:
            raise forms.ValidationError("两次密码不相同")
        return password

class ChangeUserImageForm(forms.Form):
    image = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(ChangeUserImageForm, self).__init__(*args, **kwargs)




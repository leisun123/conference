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

from crispy_forms.bootstrap import StrictButton, InlineField, InlineCheckboxes
from crispy_forms.layout import Layout, Submit, Div, ButtonHolder, HTML, Fieldset, BaseInput
from django import forms
from django.contrib import auth
from apps.accounts.models import Scholar
from crispy_forms.helper import FormHelper




class LoginForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
    
    class Meta:
        model = Scholar
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3 control-label'
        self.helper.field_class = 'col-sm-9'
        self.helper.layout = Layout(
            'email',
            'password',
            'remember_me',
            Div(
                Div(
                    HTML("<a href='{% url 'password_reset' %}'>forget password?</a>"),
                    css_class='col-sm-offset-3 col-sm-9'
                ),
                css_class='form-group'
            ),
            
            Div(
                Div(
                    Submit('Sign in', value='login', css_class='btn-default'),
                    css_class='col-sm-offset-3 col-sm-9'
                ),
                css_class='form-group'
            ),
        )

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
    
    password = forms.CharField(widget=forms.PasswordInput())
    res_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Scholar
        fields = ('first_name', 'last_name', 'organization', 'email',)

    def __init__(self, *args, **kwargs):
        self.user = None
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3 control-label'
        self.helper.field_class = 'col-sm-9'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'organization',
            'email',
            'password',
            'res_password',
            Div(
                Div(
                    Submit('Register', value='register', css_class='btn-default'),
                    css_class='col-sm-offset-3 col-sm-9'
                ),
                css_class='form-group'
            ),
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Scholar.objects.get(email=email)
            raise forms.ValidationError('Sorry,the email address has been registered ')
        except Scholar.DoesNotExist:
            return email

    def clean_res_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('res_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Inconsistent password entered twice')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['first_name'] + self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class PasswordChangeForm(forms.Form):
    
    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    res_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Scholar
        fields = ['old_password', 'password', 'res_password',]

    def __init__(self, *args, **kwargs):
        self.user = None
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3 control-label'
        self.helper.field_class = 'col-sm-9'
        self.helper.layout = Layout(
            'old_password',
            'password',
            'res_password',
            Div(
                Div(
                    Submit('Submit', value='submit', css_class='btn-default'),
                    css_class='col-sm-offset-3 col-sm-9'
                ),
                css_class='form-group'
            ),
        )
        
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        res_password = self.cleaned_data.get("res_password")
        if password and res_password and password != res_password:
            raise forms.ValidationError('Inconsistent password entered twice')
        return password

class ChangeUserImageForm(forms.Form):
    image = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(ChangeUserImageForm, self).__init__(*args, **kwargs)




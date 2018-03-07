#coding:utf-8
"""
@file:      forms
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    02/03/2018 3:20 AM
@description:
            --
"""
from itertools import chain

from django import forms
from django.forms import fields, formsets, inlineformset_factory
from guardian.shortcuts import assign_perm

from apps.accounts.models import Scholar
from .models import Paper, SpecialSession, Assignment, Review, Author, Keywords
from conference import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

class PaperForm(forms.ModelForm):
    
    session = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=SpecialSession.objects, empty_label=None)
    
    
    class Meta:
        model = Paper
        fields = ('title',  'abstract', 'file', 'session')
        
    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.template = 'bootstrap3/uni_form.html'
        self.helper.form_method = 'post'
        



class AuthorForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = ('name', 'organization', 'email', 'index')
        
AuthorFormset = formsets.formset_factory(AuthorForm, extra=1)


class KeywordsForm(forms.ModelForm):
    
    class Meta:
        model = Keywords
        fields = ('keyword',)
        
KeywordsFormset = formsets.formset_factory(KeywordsForm, extra=1)


class MyFormSetHelper(FormHelper):
    
    def __init__(self, *args, **kwargs):
        super(MyFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.template = 'bootstrap3/my_table_formset.html'
        
mylinehelper = MyFormSetHelper()

class AssignmentForm(forms.ModelForm):
    
    
    STATUS_CHOICES = (
        ('2', 'accpet'),
        ('3', 'revision'),
        ('4', 'reject'),
    )

    status = forms.ChoiceField(widget=forms.RadioSelect, choices=STATUS_CHOICES, required=True)

    class Meta:
        model = Assignment
        fields = ('status', 'proposal_to_author', )
        
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['proposal_to_author'].required = False
        self.helper = FormHelper()
        self.helper.template = 'bootstrap3/uni_form.html'
        self.helper.form_method = 'post'
        
InlineReviewFormset = inlineformset_factory(Assignment, Review, fields=('reviewer',),
                                            widgets={'reviewer': forms.Select(attrs={'required': 'required'})}, extra=1, can_delete=False)


class ReviewForm(forms.ModelForm):

     class Meta:
         model = Review
         fields = ('recommandation', 'confidentia_proposal_to_editor', 'proposal_to_author',)

     def __init__(self, *args, **kwargs):
         super(ReviewForm, self).__init__(*args, **kwargs)
         self.fields['confidentia_proposal_to_editor'].required = False
         self.fields['proposal_to_author'].required = False
         self.helper = FormHelper()
         self.helper.template = 'bootstrap3/uni_form.html'
         self.helper.form_method = 'post'
 


     def save(self, commit=False):
         self.get_object().recommandation = self.cleaned_data['recommandation']
         self.get_object().confidentia_proposal_to_editor = self.cleaned_data['confidentia_proposal_to_editor']
         self.get_object().proposal_to_author = self.cleaned_data['proposal_to_author']
         
         #TODO: Signnal
         if all([review.recommandation for review in self.get_object().assignment.review_set.all()]):
            self.get_object().assignment.status = '5'
           
 
         self.get_object().save()
        
         
         return







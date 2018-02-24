#coding:utf-8
"""
@file:      forms
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/2/2 下午7:30
@description:
            --
"""
from django import forms
from django.utils import timezone

from apps.thesis.models import Thesis, Review
from apps.accounts.models import Scholar

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


error_messages = {
    'title': {
        'required': '论文标题不能为空'
    },
    'content': {
        'required': '文件不能为空'
    },
    'keywords': {
        'required': '关键词不能为空'
    },
    'abstract': {
        'required': '简介不能为空'
    }
}

class ThesisUploadForm(forms.ModelForm):
    
    title = forms.CharField(label='论文题目', error_messages=error_messages.get('title'), required=True)
    content = forms.FileField(validators=[validate_file_extension], error_messages=error_messages.get('content'), required=True)
    keywords = forms.CharField(label="关键词", max_length=64, required=True, error_messages=error_messages.get('keywords'))
    abstract = forms.CharField(widget=forms.Textarea, max_length=256, required=True, error_messages=error_messages.get('abstract'))
    
    class Meta:
        model = Thesis
        fields = ('title', 'content', 'keywords', 'abstract')
        
    
    def save(self, request, commit=False):
        title = self.cleaned_data["title"]
        content = self.cleaned_data["content"]
        author = Scholar.objects.get(username=request.user)
        keywords = self.cleaned_data["keywords"]
        abstract = self.cleaned_data["abstract"]
        
        thesis = Thesis(
            title = title,
            content = content,
            author = author,
            keywords = keywords,
            abstract = abstract
        )
        thesis.save()
        return thesis
    
class ThesisReviewForm(forms.ModelForm):
    
    CONCLUSION_CHOICES = (
        ('1', '通过'),
        ('2', '修改'),
        ('3', '拒绝'),
    )

    conclusion = forms.ChoiceField(required=True, choices=CONCLUSION_CHOICES)
    proposal = forms.CharField(widget=forms.Textarea, max_length=256, required=True)
    
    class Meta:
        model = Review
        fields = ('conclusion', 'proposal')
    
    
    def save(self, thesis_id, commit=False):
        conclusion = self.cleaned_data['conclusion']
        proposal = self.cleaned_data['proposal']
        finish_time = timezone.now()
        review = Review.objects.filter(thesis_id=thesis_id).update(conclusion=conclusion, proposal=proposal, finish_time=finish_time)
        return review
        
        
    
    
        
        
        
        
        
        
        
        
        
        
        
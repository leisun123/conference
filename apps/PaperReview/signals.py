#coding:utf-8
"""
@file:      signals
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    10/03/2018 10:52 PM
@description:
            --
"""
import django.dispatch
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save
from django.template.loader import get_template

from apps.mail.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from guardian.shortcuts import assign_perm
import random
from apps.PaperReview.models import Assignment, Review

paper_save_signal = django.dispatch.Signal(providing_args=['request', 'paper_object'])
paper_update_signal = django.dispatch.Signal(providing_args=['request', 'new_paper_object', 'old_paper_object'])
assignment_save_signal = django.dispatch.Signal(providing_args=['reviews','object'])

data = {'scholarname':'wang'}

email_content = get_template('share_layout/email.html').render(data)


@receiver(pre_save,sender=paper_save_signal)
def paper_save_callback(sender, **kwargs):
    
    editors = Group.objects.get(name="editor").user_set.all()
    editor = random.choice(editors)
    
    assignment = Assignment.objects.create(editor=editor, paper=kwargs['paper_object'])
    
    assign_perm('PaperReview.view_paper', kwargs['request'].user, kwargs['paper_object'])
    assign_perm('PaperReview.view_paper', editor, kwargs['paper_object'])
    assign_perm('PaperReview.view_assignment', editor, assignment)
    assign_perm('PaperReview.create_assignment', editor, assignment)
    
    
    send_mail(subject="123", body="123", from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['genius_wz@aliyun.com', ], fail_silently=False,
                  html=email_content)
    
    
@receiver(pre_save, sender=paper_update_signal)
def paper_update_callback(sender, **kwargs):
    
    request = kwargs['request']
    new_paper_object = kwargs['new_paper_object']
    old_paper_object = kwargs['old_paper_object']
    
    lastest_assignment_object = Assignment.objects.get(id=1)
    
    if lastest_assignment_object.status == '3':
        lastest_review_set = [Review.objects.create(reviewer=review.reviewer) for review in
                              lastest_assignment_object.review_set().all()]
        lastest_assignment_object = Assignment.objects.create(editor=lastest_assignment_object.editor,
                                                              paper=new_paper_object)
        lastest_assignment_object.review_set.set(lastest_review_set)
        
        send_mail(subject="123", body="123", from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['genius_wz@aliyun.com', ], fail_silently=False,
                  html=email_content)
        
    assign_perm('PaperReview.view_paper', request.user, old_paper_object)
    assign_perm('PaperReview.view_paper', lastest_assignment_object.editor, old_paper_object)
    assign_perm('PaperReview.view_assignment', lastest_assignment_object.editor, lastest_assignment_object)
    assign_perm('PaperReview.create_assignment', lastest_assignment_object.editor, lastest_assignment_object)
    
@receiver(pre_save, sender=assignment_save_signal)
def assignment_save_callback(sender, **kwargs):
    for review in kwargs['reviews']:
        review_object = Review.objects.create(reviewer=review['reviewer'], assignment=kwargs['object'])
        review_object.reviewer.groups.add(Group.objects.get(name="reviewer"))
        
        assign_perm('view_paper', review['reviewer'], kwargs['object'].paper)
        assign_perm('view_review', review['reviewer'], review_object)
        assign_perm('create_review', review['reviewer'], review_object)







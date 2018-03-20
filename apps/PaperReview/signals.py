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
import os
from django.contrib.auth.models import Group
from django.template.loader import get_template
from apps.mail.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from guardian.shortcuts import assign_perm
import random
from apps.PaperReview.models import Assignment, Review, Paper

paper_save_signal = django.dispatch.Signal(providing_args=['request', 'paper_object'])
paper_update_signal = django.dispatch.Signal(providing_args=['request', 'new_paper_object', 'old_paper_object'])
assignment_save_signal = django.dispatch.Signal(providing_args=['reviews','object'])


@receiver(paper_save_signal)
def paper_save_callback(sender, **kwargs):
    
    
    new_name = 'thesis/{}.pdf'.format(kwargs['paper_object'].serial_number)
    os.rename(kwargs['paper_object'].file.path, os.path.join(settings.MEDIA_ROOT, new_name))
    kwargs['paper_object'].file.name = new_name
    kwargs['paper_object'].save()
    
    editors = Group.objects.get(name="editor").user_set.all()
    editor = random.choice(editors)
    
    assignment = Assignment.objects.create(editor=editor, paper=kwargs['paper_object'])
    
    assign_perm('PaperReview.view_paper', kwargs['request'].user, kwargs['paper_object'])
    assign_perm('PaperReview.view_paper', editor, kwargs['paper_object'])
    assign_perm('PaperReview.view_assignment', editor, assignment)
    assign_perm('PaperReview.create_assignment', editor, assignment)
    
    data = {'id': kwargs['paper_object'].id, 'title': kwargs['paper_object'].title, 'version': kwargs['paper_object'].version}
    email_content = get_template('email/submission.html').render(data)
    send_mail(subject="CSQRWC TEAM", body="", from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[kwargs['paper_object'].uploader.email,], fail_silently=False,
                  html=email_content)
    

@receiver(paper_update_signal)
def paper_update_callback(sender, **kwargs):
    
    request = kwargs['request']
    new_paper_object = kwargs['new_paper_object']
    old_paper_object = kwargs['old_paper_object']
    
    lastest_assignment_object = old_paper_object.assignment
    lastest_review_set = kwargs['lastest_review_set']
    
    if lastest_assignment_object.status == '3':
        lastest_review_set = [Review.objects.create(reviewer=review.reviewer) for review in
                              lastest_review_set]
        lastest_assignment_object = Assignment.objects.create(editor=lastest_assignment_object.editor,
                                                              paper=new_paper_object)
        lastest_assignment_object.review_set.set(lastest_review_set)
        
        #TODO
        data = {'id':old_paper_object.paper.id, 'title': old_paper_object.title, 'version': kwargs['paper_object'].version}
        email_content = get_template('email/submission.html').render(data)
        send_mail(subject="CSQRWC TEAM", body="", from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[review.reviewer.email for review in lastest_review_set], fail_silently=False,
                  html=email_content)
    
        
    assign_perm('PaperReview.view_paper', request.user, new_paper_object)
    assign_perm('PaperReview.view_paper', lastest_assignment_object.editor, new_paper_object)
    
    assign_perm('PaperReview.view_assignment', lastest_assignment_object.editor, lastest_assignment_object)
    assign_perm('PaperReview.create_assignment', lastest_assignment_object.editor, lastest_assignment_object)

    
@receiver(assignment_save_signal)
def assignment_save_callback(sender, **kwargs):
    
    for review in kwargs['reviews']:
        review_object = Review.objects.create(reviewer=review['reviewer'], assignment=kwargs['object'])
        review_object.reviewer.groups.add(Group.objects.get(name="reviewer"))
        
        assign_perm('view_paper', review['reviewer'], kwargs['object'].paper)
        assign_perm('view_review', review['reviewer'], review_object)
        assign_perm('create_review', review['reviewer'], review_object)
        
        data = {'id':kwargs['object'].paper.id, 'title': kwargs['object'].paper.title,\
                'name': review['reviewer'].username, 'email':review['reviewer'].email, 'password':review['reviewer'].email }
        
        email_content = get_template('email/first_review.html').render(data) \
                    if review['reviewer'].is_assigned_password else get_template('email/review.html').render(data)
        
        send_mail(subject="CSQRWC TEAM", body="", from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[review['reviewer'].email,], fail_silently=False,
                  html=email_content)
      
    data = {'id':kwargs['object'].paper.id, 'title': kwargs['object'].paper.title,
            'username': kwargs['object'].paper.uploader.username,
            'reviews': kwargs['object'].review_set.all()}
    if kwargs['object'].status == '2':
        email_content = get_template('email/accpect.html').render(data)
    elif kwargs['object'].status == '3':
        email_content = get_template('email/revise.html').render(data)
    elif kwargs['object'].status == '4':
        email_content = get_template('email/reject.html').render(data)
    else:
        email_content = None
    
    if email_content:
        send_mail(subject="CSQRWC TEAM", body="", from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[kwargs['object'].paper.uploader.email,], fail_silently=False,
                  html=email_content)
    
    
    

    

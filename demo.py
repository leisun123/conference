#coding:utf-8
"""
@file:      demo.py
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    1/5/18 10:23 AM
@description:
            --
"""
import os
import django



SETTINGS = 'conference.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS






def main():
    django.setup()
    
    from django.contrib.auth.models import Group
    from apps.accounts.models import Scholar
    
    submitter = Group.objects.create(name='Submitter')
    editor  = Group.objects.create(name='Editor')
    reviewer = Group.objects.create(name='Reviewer')

    wz1 = Scholar.objects.create_user(
        'wyn1',
        'wyn1@aliyun.com',
        '123456'
    )
    wz2 = Scholar.objects.create_user(
        'wyn2',
        'wyn2@aliyun.com',
        '123456'
    )
    wz3 = Scholar.objects.create_user(
        'wyn3',
        'wyn3@aliyun.com',
        '123456'
    )
    submitter.user_set.add(wz1)
    reviewer.user_set.add(wz2)
    editor.user_set.add(wz3)
    #
    # scholar = Group.objects.create(name='Scholar')
    
if __name__ == '__main__':
    main()





















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
    
    from apps.PaperReview.models import Review,Author,SpecialSession,Assignment,Keywords,Paper
    from apps.accounts.models import Scholar
    from django.contrib.auth.models import Group, User
    from guardian.shortcuts import remove_perm
    from guardian.shortcuts import assign_perm
    from django.core.files import File
    from apps.PaperReview.signals import paper_save_signal
    from apps.PaperReview.views import PaperCreateView
    
    #file=File(open('/Users/wyn/wynproject/conference/media/thesis/计划财务处信息门户11-5.pdf', 'rb'))
    # # Content.objects.filter(id=1).update(version=2)
    # c = Content.objects.get(id=1)
    # c.version = 3
    # print(c.tracker.has_changed('version'))
    # print(c.tracker.changed())
    
    #scholar = Group.objects.create(name='scholar')
    #reviewer = Group.objects.create(name='reviewer')
    editor = Group.objects.create(name='editor')

    Scholar.objects.create_superuser(username='wyn', email='isolationwyn@gmail.com', password='python123')
    editor.user_set.add(Scholar.objects.create_superuser(username='Lei Zhao', email='leizhao@jsnu.edu.cn', password='leizhao@jsnu.edu.cn'))
    

    
if __name__ == '__main__':
    main()
    




















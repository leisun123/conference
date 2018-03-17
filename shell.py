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
    #file=File(open('/Users/wyn/wynproject/conference/media/thesis/计划财务处信息门户11-5.pdf', 'rb'))
    # # Content.objects.filter(id=1).update(version=2)
    # c = Content.objects.get(id=1)
    # c.version = 3
    # print(c.tracker.has_changed('version'))
    # print(c.tracker.changed())
    
    scholar = Group.objects.get(name='scholar')
    reviewer = Group.objects.get(name='reviewer')
    editor = Group.objects.get(name='editor')
    #
    # #Scholar.objects.create_user(username='ed1',email='ed1@gmail.com', password='python123')
    # Scholar.objects.create_user(username='ed2',email='ed2@gmail.com', password='python123')
    # session_list=['Computational Electromagnetic Methods','Electromagnetic Theory and Propagation','Electromagnetic Theory and Propagation',
    #  '4G/5G Wireless or Mobile Systems','Micro and Millimeter Wave Measurement Technique','Microwave Remote Sensing','Photonics',
    #  'Metamaterial','Plasmonic','Antenna Theory and Technique','Microwave / Millimeter Circuits and Devices','EMI/EMC','RFID Systems',
    #  'Imaging and Signal Processing','Bioelectromagnetics','Mobile Network and Internet','Electromagnetic Properties of Materials',
    #  'Internet of Things','Internet and Computer Applications','Wireless Access','Sensor Networks','Software Defined Radio','Radar Systems','Others']
    # for i in session_list:
    #     SpecialSession.objects.get_or_create(name=i)

    #Scholar.objects.create_superuser(username='wyn', email='isolationwyn@gmail.com', password='python123')
    
    #editor.user_set.add(Scholar.objects.get(email='isolationwyn@gmail.com'))
    
    editor.user_set.add(Scholar.objects.get(email='genius_wz@aliyun.com'))
    
if __name__ == '__main__':
    main()
    





















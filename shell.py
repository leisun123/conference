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
    
    scholar = Group.objects.create(name='scholar')
    reviewer = Group.objects.create(name='reviewer')
    editor = Group.objects.create(name='editor')

    Scholar.objects.create_superuser(username='wyn', email='isolationwyn@gmail.com', password='python123')
    
    
    list = ['Ke Gong-- Microwave/millimeter wave integrated antennas',
        'Long Li, Huiqing Zhai and Yan Shi-- 5G Communication Antennas, Metamaterials, andMetasufaces',
            'Tao Li, Xuejin Zhang and Changchun Yan-- Nanophotonics and Plasmonics',
        'Weidong Li-- Numerical methods and their fast algorithms for electromagnetic fields',
        'Yongjin Zhou and Kaida Xu-- Plasmonic metamaterials and applications',
        'Qiang Cheng-- Artificial Metamaterials and Metasurfaces',
        'Zhixiang Huang and Wei Sha-- Nonlinear Electromagnetics',
        'Yue Li and Guqing Luo-- Advanced Techniques on Antennas and Metamaterials',
        'Luyu Zhao-Compact and High Performance Antenna Design for Next Generation Mobile Devices',
        'Ning Su and Yue Jin-- Multimedia Information Processing',
        'Jian Li and Yongjun Huang-- New devices and systems of Internet of Things (IoT)',
        'Lisheng Xu and Zedong Nie-- Body sensor network for healthcare application',
        'Shengjun Zhang and Yumao Wu-- Active Periodic Structures, FSS and Metamaterials',
        'Zhenbao Ye and Xunwang Zhao-- High Performance Multi-Scale/Multi- Physics Computing',
        'Methods for Simulating Complex EM Environment Effects',
        'Xiuzhu Ye and Kuiwen Xu-- New Electromagnetic Imaging Technique and System']
    for i in list:
        SpecialSession.objects.create(name=i)
    
    
    
    session_list=['Computational Electromagnetic Methods','Electromagnetic Theory and Propagation',
     '4G/5G Wireless or Mobile Systems','Micro and Millimeter Wave Measurement Technique','Microwave Remote Sensing','Photonics',
     'Metamaterial','Plasmonic','Antenna Theory and Technique','Microwave / Millimeter Circuits and Devices','EMI/EMC','RFID Systems',
     'Imaging and Signal Processing','Bioelectromagnetics','Mobile Network and Internet','Electromagnetic Properties of Materials',
     'Internet of Things','Internet and Computer Applications','Wireless Access','Sensor Networks','Software Defined Radio','Radar Systems','Others']
    for i in session_list:
        SpecialSession.objects.create(name=i)

 

    
    
if __name__ == '__main__':
    main()





















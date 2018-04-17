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
    from apps.PaperReview.models import Assignment, Review
    from apps.accounts.models import Scholar
    from apps.accounts.models import SpecialSession
    from apps.PaperReview.models import Review,Author,SpecialSession,Assignment,Keywords,Paper
    from apps.accounts.models import Scholar
    from django.contrib.auth.models import Group, User
    from guardian.shortcuts import remove_perm
    from guardian.shortcuts import assign_perm
    from django.core.files import File
    from apps.PaperReview.signals import paper_save_signal
    from apps.PaperReview.views import PaperCreateView
    
    #Group.objects.create(name='scholar')
    #Group.objects.create(name='reviewer')
    #Group.objects.create(name='editor')
    
   #  Group.objects.get(name='editor').user_set.add(
   #      Scholar.objects.create_user(username='Lei Zhao', email='leizhao@jsnu.edu.cn', password='leizhao@jsnu.edu.cn'))
   #
   #  list = ['Ke Gong-- Microwave/millimeter wave integrated antennas',
   #    'Long Li, Huiqing Zhai and Yan Shi-- 5G Communication Antennas, Metamaterials, andMetasufaces',
   #        'Tao Li, Xuejin Zhang and Changchun Yan-- Nanophotonics and Plasmonics',
   #    'Weidong Li-- Numerical methods and their fast algorithms for electromagnetic fields',
   #    'Yongjin Zhou and Kaida Xu-- Plasmonic metamaterials and applications',
   #    'Qiang Cheng-- Artificial Metamaterials and Metasurfaces',
   #    'Zhixiang Huang and Wei Sha-- Nonlinear Electromagnetics',
   #    'Yue Li and Guqing Luo-- Advanced Techniques on Antennas and Metamaterials',
   #    'Luyu Zhao-Compact and High Performance Antenna Design for Next Generation Mobile Devices',
   #    'Ning Su and Yue Jin-- Multimedia Information Processing',
   #    'Jian Li and Yongjun Huang-- New devices and systems of Internet of Things (IoT)',
   #    'Lisheng Xu and Zedong Nie-- Body sensor network for healthcare application',
   #    'Shengjun Zhang and Yumao Wu-- Active Periodic Structures, FSS and Metamaterials',
   #    'Zhenbao Ye and Xunwang Zhao-- High Performance Multi-Scale/Multi- Physics Computing',
   #    'Methods for Simulating Complex EM Environment Effects',
   #    'Xiuzhu Ye and Kuiwen Xu-- New Electromagnetic Imaging Technique and System']
   #  for i in list:
   #     SpecialSession.objects.create(name=i)
   #
   #
   #  session_list=['Computational Electromagnetic Methods','Electromagnetic Theory and Propagation',
   # '4G/5G Wireless or Mobile Systems','Micro and Millimeter Wave Measurement Technique','Microwave Remote Sensing','Photonics',
   # 'Metamaterial','Plasmonic','Antenna Theory and Technique','Microwave / Millimeter Circuits and Devices','EMI/EMC','RFID Systems',
   # 'Imaging and Signal Processing','Bioelectromagnetics','Mobile Network and Internet','Electromagnetic Properties of Materials',
   # 'Internet of Things','Internet and Computer Applications','Wireless Access','Sensor Networks','Software Defined Radio','Radar Systems','Others']
   #  for i in session_list:
   #     SpecialSession.objects.create(name=i)
   #
    
    
    
    paper = Paper.objects.get(id=68)
    assignment = Assignment.objects.get(paper=paper)
    scholar = Scholar.objects.get(id=129)
    review_object = Review.objects.create(reviewer=scholar, assignment=assignment)
    review_object.reviewer.groups.add(Group.objects.get(name="reviewer"))
    
    assign_perm('view_paper', scholar, paper)
    assign_perm('view_review', scholar, review_object)
    assign_perm('create_review', scholar, review_object)
   
   
if __name__ == '__main__':
    main()
    




















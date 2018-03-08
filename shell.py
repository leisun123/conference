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
    from django.contrib.auth.models import Group
    
    from django.core.files import File
    #file=File(open('/Users/wyn/wynproject/conference/media/thesis/计划财务处信息门户11-5.pdf', 'rb'))
    # # Content.objects.filter(id=1).update(version=2)
    # c = Content.objects.get(id=1)
    # c.version = 3
    # print(c.tracker.has_changed('version'))
    # print(c.tracker.changed())
    
    
    wz1=Scholar.objects.get(username="wz1")
    wz2=Scholar.objects.get(username="wz2")
    wz3=Scholar.objects.get(username="wz3")
    wz4=Scholar.objects.get(username="wz4")
    wz5=Scholar.objects.get(username="wz5")
    
    wzed1=Scholar.objects.get(username="wzed1")
    wzed2=Scholar.objects.get(username="wzed2")
    wzed3=Scholar.objects.get(username="wzed3")
    wzrw1=Scholar.objects.get(username="wzrw1")
    wzrw2=Scholar.objects.get(username="wzrw2")
    wzrw3=Scholar.objects.get(username="wzrw3")

    
    #Group.objects.create(name="editor")
    #Group.objects.create(name="reviewer")
    
    #Group.objects.get(name="scholar").user_set.set([wz1, wz2, wz3, wz4, wz5])
    
    # SpecialSession.objects.create(name="session1")
    # SpecialSession.objects.create(name="session2")
    # SpecialSession.objects.create(name="session3")
    # SpecialSession.objects.create(name="session4")
    
    session1=SpecialSession.objects.get(name="session1")
    session2=SpecialSession.objects.get(name="session2")
    session3=SpecialSession.objects.get(name="session3")
    session4=SpecialSession.objects.get(name="session4")
    
    # SpecialSession.objects.get(name="session1").scholar_set.set([wzrw1, wzrw2])
    # SpecialSession.objects.get(name="session2").scholar_set.set([wzrw1, wzrw3])
    # SpecialSession.objects.get(name="session3").scholar_set.set([wzrw2, wzrw3])
    # SpecialSession.objects.get(name="session4").scholar_set.set([wzrw2])
    
    

    #paper1=Paper.objects.create(title="foo1",file=file,abstract="abstract", uploader=wz1, session=session1)
    
    #paper1=Paper.objects.get(title="foo1")
  
    # a1 = {"name": "a1", "organization": "jsnu", "email": "117188@qq.com", "index":1, "paper": paper1}
    # a2 = {"name": "a2", "organization": "jsnu", "email": "117188@qq.com", "index":1, "paper": paper1}
    # a3 = {"name": "a3", "organization": "jsnu", "email": "117188@qq.com", "index":1, "paper": paper1}
    # a4 = {"name": "a4", "organization": "jsnu", "email": "117188@qq.com", "index":1, "paper": paper1}
    #
    # Author.objects.create(**a2)
    # Author.objects.create(**a3)
    # Author.objects.create(**a4)
    

    #
    # k1=Keywords.objects.create(keyword="k1", paper=paper1)
    # k2=Keywords.objects.create(keyword="k2", paper=paper1)
    # k3=Keywords.objects.create(keyword="k3", paper=paper1)


    #asm = Assignment.objects.get(id=1)

    #Review.objects.create(reviewer=wzrw1, recommandation="1", assignment=asm)
    
    editors = Group.objects.get(name="editor").user_set.all()
    
    
    from django.contrib.auth.models import User,Group,Permission
    from django.contrib.contenttypes.models import ContentType
    
    # content_type = ContentType.objects.get(app_label='PaperReview', model='paper')
    # permission = Permission.objects.create(codename='create_paper',
    #                                    name='Can Create Paper',
    #                                    content_type=content_type)
    
    permission = Permission.objects.get(codename='view_paper')
    #group = Group.objects.get(name='scholar')
    #group.permissions.add(permission)
    # print(wz1.has_perm('PaperReview.view_paper'))
    # print(wz1.has_perm('PaperReview.create_paper'))
    # [print(i) for i in wz1.get_group_permissions()]
    paper = Paper.objects.get(id=1)
    tmp = Paper.objects.get(id=1)._meta.get_fields()
    # [print(field.name, getattr(paper, field.name)
    #     if field.concrete else [([print(j.name) for j in i._meta.get_fields( )  if not j.auto_created]) for i in field.related_model.objects.filter(paper=paper).all()  ]
    #             ) for field in tmp
    #     ]
    # #
    # def display_data(instance):
    #     def get_all_fields(instance):
    #
    #         for field in instance._meta.get_fields():
    #
    #                 if field.concrete and not field.auto_created \
    #                         and not field.one_to_one and not field.one_to_many:
    #                    print(field.name, getattr(instance, field.name))
    #                 elif field is not None:
    #                     foreignkey_name = type(instance).__name__.lower()
    #                     print(foreignkey_name)
    #
    #                     for i in field.related_model.objects.filter(**{foreignkey_name:instance}):
    #
    #                             get_all_fields(i)
    #
    #     return get_all_fields(instance)
    #
    #
    #
    #
    # paper = Paper.objects.get(id=1)
    # #print(type(paper).__name__)
    # display_data(paper)
    
    # from itertools import chain
    # print(list(set(chain.from_iterable(
    #     (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
    #     for field in paper._meta.get_fields()
    #     # For complete backwards compatibility, you may want to exclude
    #     # GenericForeignKey from the results.
    #     if not (field.many_to_one and field.related_model is None)
    # ))))
    [print(i.name) for i in wz1.groups.all()]
    # review = Review.objects.get(id=2)
    # if review.recommandation:
    #     print(1111)
    # else:
    #     print(22222)
    
if __name__ == '__main__':
    main()
    





















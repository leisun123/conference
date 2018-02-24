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
    from apps.thesis.models import Review, Thesis
    wyn = Scholar.objects.get(username="wyn")
    wzz = Scholar.objects.get(username="wzz")
    zzw = Scholar.objects.get(username="zzw")
    # thesis = Thesis.objects.create(title="zwzzzz", content="/Users/wyn/wynproject/conference/media/thesis/计划财务处信息门户.pdf",
    #        author=wyn, keywords="ww", abstract="ww")
    thesis = Thesis.objects.get(id=2)
    
    Review.objects.create(reviewer=zzw, thesis=thesis, conclusion=1, proposal="wewe")
    
    {% for i in review.reviewer %}
							<option data-tokens="{{ i.username }}" data-subtext="{{ i.organization }}">{{ i.username }}</option>
  							{% endfor %}
if __name__ == '__main__':
    main()





















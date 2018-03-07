"""Model definition for test workflow"""

from django.db.models import (
    CharField,
    ForeignKey,
    IntegerField,
    TextField)

from apps.accounts.models import Scholar
from apps.activflow.models import (
    AbstractEntity,
    AbstractActivity,
    AbstractInitialActivity)

from apps.thesisReview.validators import validate_initial_cap


class Upload(AbstractInitialActivity):

    thesis_title = CharField("论文题目", max_length=200)
    content = TextField("论文", max_length=1000)
    keywords = CharField("关键词", max_length=200)
    abstract = TextField("概述", max_length=200)


    def clean(self):
        """Custom validation logic should go here"""
        pass

class Distribution(AbstractActivity):

    REVIEWER_STATUS = (
        ('Wz', 'Wangzi'),
        ('wz2', 'wangzi2')
    )
    reviewer1 = CharField(verbose_name="reviewer1", max_length=30, choices=REVIEWER_STATUS)
    reviewer2 = CharField(verbose_name="reviewer2", max_length=30, choices=REVIEWER_STATUS)
    reviewer3 = CharField(verbose_name="reviewer3", max_length=30, choices=REVIEWER_STATUS)

    @property
    def title(self):
        """Returns entity title"""
        return self.__class__.__name__

    def clean(self):
        """Custom validation logic should go here"""
        pass


CONCLUSION_CHOICES = (
        ('1', '通过'),
        ('2', '修改'),
        ('3', '拒绝'),
    )

class Review(AbstractActivity):


    conclusion = CharField(verbose_name="终审", max_length=30, choices=CONCLUSION_CHOICES)

    @property
    def title(self):
        """Returns entity title"""
        return self.__class__.__name__

from django.db import models
class ReviewLine(AbstractEntity):
    """Sample representation of Foo Line Item"""
    review = ForeignKey(Review, on_delete=models.CASCADE, related_name="lines")
    result = CharField(verbose_name="初审", max_length=30, choices=CONCLUSION_CHOICES)

    @property
    def title(self):
        """Returns entity title"""
        return self.__class__.__name__

    def clean(self):
        """Custom validation logic should go here"""
        pass

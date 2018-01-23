from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.urlresolvers import reverse

class Scholar(AbstractUser):
    avatar = models.ImageField('头像', upload_to='avatars', blank=True)
    organization = models.CharField(verbose_name='组织',max_length=200, blank=False)
    keywords = models.CharField(verbose_name='关键词',max_length=200, blank=False)
    major = models.TextField(verbose_name='简介', max_length=500, blank=False)
    
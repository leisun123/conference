from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class SpecialSession(models.Model):
    
    name = models.CharField(unique=True, max_length=128)
    
    def __str__(self):
        return self.name

class Scholar(AbstractUser):
    
    USERNAME_FIELD = 'email'
    
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True)
    organization = models.CharField(verbose_name='组织',max_length=200, blank=False)
    keywords = models.CharField(verbose_name='关键词',max_length=200, blank=False)
    major = models.TextField(verbose_name='简介', max_length=500, blank=False)
    session = models.ForeignKey(SpecialSession, null=True, on_delete=models.SET_NULL)
    REQUIRED_FIELDS = []
    
    class Meta(object):
        unique_together = ('email',)
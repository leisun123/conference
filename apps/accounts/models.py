from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class SpecialSession(models.Model):
    
    name = models.CharField(unique=True, max_length=128)
    
    def __str__(self):
        return self.name

class Scholar(AbstractUser):
    
    USERNAME_FIELD = 'email'
    
    username = models.CharField(max_length=8, null=True, blank=True)
    email = models.EmailField(blank=False, unique=True)
    avatar = models.ImageField('avatar', upload_to='avatars/', blank=True)
    organization = models.CharField(verbose_name='organization',max_length=200, blank=False)
    session = models.ForeignKey(SpecialSession, null=True, on_delete=models.SET_NULL)
    
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
    
    # class Meta(object):
    #     unique_together = ('email',)
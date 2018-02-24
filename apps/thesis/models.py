import os
from django.db import models

# Create your models here.
from django.utils.text import slugify
from apps.accounts.models import Scholar

class BaseModel(models.Model):
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.slug or self.slug == 'no-slug' or not self.id:
            slug = self.title if 'title' in self.__dict__ else self.name
            self.slug = slugify(slug)
        super().save(*args, **kwargs)
        # type = self.__class__.__name__
        
    class Meta:
        abstract = True
        

class Thesis(BaseModel):
    
    STATUS_CHOICES = {
        0: u'未分配',
        1: u'审核中',
        2: u'通过',
        3: u'修改',
        4: u'拒绝',
    }
    
    title = models.CharField(max_length=128)
    content = models.FileField(upload_to='thesis/')
    author = models.ForeignKey(Scholar, related_name="thesis_author")
    handle_memebers = models.ManyToManyField(Scholar, through='Review')
    status = models.CharField(verbose_name="论文状态", max_length=64, choices=STATUS_CHOICES.items(), default=0)
    keywords = models.CharField(verbose_name="关键词", max_length=64)
    abstract = models.TextField(verbose_name="概述", max_length=256)
    create_time = models.DateField(verbose_name="创建时间",auto_now_add=True)
    publish_time = models.DateField(verbose_name="发布时间", null=True)
 

    
class Review(models.Model):
    
    CONCLUSION_CHOICES = (
        ('1', '通过'),
        ('2', '修改'),
        ('3', '拒绝'),
    )
    
    reviewer = models.ForeignKey(Scholar, null=True)
    thesis = models.ForeignKey(Thesis)
    conclusion = models.CharField(verbose_name="初步结论", max_length=64, choices=CONCLUSION_CHOICES, null=True)
    proposal = models.TextField(verbose_name="建议", max_length=1024, null=True)
    
    create_time = models.DateField(verbose_name="分派时间",auto_now_add=True)
    finish_time = models.DateField(verbose_name="审核结束时间", null=True)
    

        


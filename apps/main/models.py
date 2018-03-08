from django.db import models
from DjangoUeditor.models import UEditorField
from django.urls import reverse, reverse_lazy
from django.utils import timezone


class SideBar(models.Model):
    node_name = models.CharField('标题', max_length=200, unique=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    rank = models.IntegerField(default=0, verbose_name=u'排序')
    parent_node = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="父级分类", blank=True, null=True)
    
    def __str__(self):
        return self.node_name
    
    class Meta:
        ordering = ['rank']
        verbose_name = "分类"
        verbose_name_plural = verbose_name
        
    def get_absolute_url(self):
        return reverse_lazy('main:genericTagContentById', kwargs={
                'content_id': self.id
            })


class GenericTagContent(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
   
    theme = models.CharField('标题', max_length=200, unique=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    body = UEditorField(verbose_name=u'正文', toolbars='full', width='600', height='300', imagePath='file/',
                        filePath='file/', default='')
    created_time = models.DateTimeField('创建时间', default=timezone.now, )
    last_mod_time = models.DateTimeField('修改时间', blank=True, null=True)
    
    sidebar = models.ForeignKey('SideBar', verbose_name='分类', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        ordering = ['last_mod_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'


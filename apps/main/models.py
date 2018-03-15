from django.db import models
from DjangoUeditor.models import UEditorField
from django.urls import reverse, reverse_lazy
from django.utils import timezone


class SideBar(models.Model):
    node_name = models.CharField('Tag Name', max_length=200, unique=True)
    rank = models.IntegerField(default=0)
    parent_node = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="parent node", blank=True, null=True)
    
    def __str__(self):
        return self.node_name
    
    class Meta:
        ordering = ['rank']
        verbose_name = "SideBar Tag"
        
    def get_parent_nodes(self):
        
        nodes = []
        
        def parse(node):
            nodes.append(node)
            if node.parent_node:
                parse(node.parent_node)
        
        parse(self)
        return nodes
    
    def get_sub_nodes(self):
        
        nodes = []
        all_nodes = SideBar.objects.all()
        
        def parse(node):
            if node not in nodes:
                nodes.append(node)
            child_nodes = all_nodes.filter(parent_node=node)
            for node in child_nodes:
                parse(node)
        parse(self)
        return nodes


class GenericTagContent(models.Model):

    title = models.CharField('title', max_length=200, unique=True)
    body = UEditorField(verbose_name='content', toolbars='full', width='600', height='300', imagePath='ad/',
                        filePath='ad/', default='')
    
    sidebar = models.ForeignKey('SideBar', verbose_name='tag name', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Tag Content"



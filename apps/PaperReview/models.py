import os
import uuid
from apps.accounts.models import Scholar, SpecialSession
from django.db import models
from django.core.validators import FileExtensionValidator
from apps.PaperReview.tracker import FieldTracker

class Paper(models.Model):

    title = models.CharField(max_length=128)
    abstract = models.TextField(max_length=1024)
    file = models.FileField(upload_to='thesis/', max_length=1024*50, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    version = models.IntegerField(default=1)
    serial_number = models.UUIDField(primary_key=False, unique=False, default=uuid.uuid4)
    
    create_time = models.DateField(auto_now_add=True)
    publish_time = models.DateField(auto_now=True)
    
    uploader = models.ForeignKey(Scholar, null=True, on_delete=models.SET_NULL)
    session = models.ForeignKey(SpecialSession, on_delete=models.CASCADE, blank=False)
    
    tracker = FieldTracker()
    
    class Meta:
        permissions = (
            ('view_paper', 'View Paper'),
            ('create_paper', 'Create Paper'),
            ('update_paper', 'Update Paper')
        )
        
class Author(models.Model):
    
    name = models.CharField(max_length=128)
    organization = models.CharField(max_length=256)
    email = models.EmailField()
    index = models.IntegerField()
    paper = models.ForeignKey(Paper, null=True, on_delete=models.CASCADE)
    tracker = FieldTracker()
    
    
class Keywords(models.Model):
    
    keyword = models.CharField(max_length=64)
    
    paper = models.ForeignKey(Paper, null=True, on_delete=models.CASCADE)
    
    tracker = FieldTracker()
    
class Assignment(models.Model):
    
    STATUS_CHOICES = (
        ('0', 'unassign'),
        ('1', 'underreview'),
        ('2', 'accpet'),
        ('3', 'revision'),
        ('4', 'reject'),
        ('5', 'waitingverdict')
    )
    
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='0')
    proposal_to_author = models.TextField(max_length=1024, null=True)
    
    editor = models.ForeignKey(Scholar, on_delete=models.CASCADE)
    paper = models.OneToOneField(Paper, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_assignment', 'View Assignment'),
            ('create_assignment', 'Create Assignment')
        )
        
    def get_status(self):
        return self.STATUS_CHOICES.get(self.status)

class Review(models.Model):
    
    RECOMMONDATION_CHOICES = (
        ('1', 'accpet'),
        ('2', 'revision'),
        ('3', 'reject')
    )
    
    recommandation = models.CharField(max_length=16, blank=False, choices=RECOMMONDATION_CHOICES)
    confidentia_proposal_to_editor = models.TextField(max_length=1024, null=True)
    proposal_to_author = models.TextField(max_length=1024, null=True, blank=True)
    create_time = models.DateField(auto_now_add=True)
    finish_time = models.DateField(auto_now=True)
    
    reviewer = models.ForeignKey(Scholar, null=True, blank=False, on_delete=models.SET_NULL)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    
    class Meta:
        permissions = (
            ('view_review', 'View Review'),
            ('create_review', 'Create Review')
        )




    

    
    
    



    

    


    

        


    

    
    

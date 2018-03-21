# Generated by Django 2.0.3 on 2018-03-21 05:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'Unassign'), ('1', 'Underreview'), ('2', 'Accpet'), ('3', 'Revision'), ('4', 'Reject'), ('5', 'WaitingVerdict')], default='0', max_length=16)),
                ('proposal_to_author', models.TextField(max_length=1024, null=True)),
            ],
            options={
                'permissions': (('view_assignment', 'View Assignment'), ('create_assignment', 'Create Assignment')),
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('organization', models.CharField(max_length=256, verbose_name='Organization')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('index', models.IntegerField(verbose_name='Index')),
            ],
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('abstract', models.TextField(max_length=1024)),
                ('file', models.FileField(max_length=400, upload_to='thesis/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Paper Resource')),
                ('copyright', models.FileField(max_length=400, upload_to='copyright/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Copyright')),
                ('version', models.IntegerField(default=1)),
                ('serial_number', models.UUIDField(default=uuid.uuid4)),
                ('create_time', models.DateField(auto_now_add=True)),
                ('publish_time', models.DateField(auto_now=True)),
            ],
            options={
                'permissions': (('view_paper', 'View Paper'), ('create_paper', 'Create Paper'), ('update_paper', 'Update Paper')),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommandation', models.CharField(choices=[('1', 'Accpet'), ('2', 'Revision'), ('3', 'Reject')], max_length=16)),
                ('confidentia_proposal_to_editor', models.TextField(max_length=1024, null=True)),
                ('proposal_to_author', models.TextField(blank=True, max_length=1024, null=True)),
                ('create_time', models.DateField(auto_now_add=True)),
                ('finish_time', models.DateField(auto_now=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PaperReview.Assignment')),
            ],
            options={
                'permissions': (('view_review', 'View Review'), ('create_review', 'Create Review')),
            },
        ),
    ]

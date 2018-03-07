# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-02 03:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activflow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('reviewer1', models.CharField(choices=[('Wz', 'Wangzi'), ('wz2', 'wangzi2')], max_length=30, verbose_name='reviewer1')),
                ('reviewer2', models.CharField(choices=[('Wz', 'Wangzi'), ('wz2', 'wangzi2')], max_length=30, verbose_name='reviewer2')),
                ('reviewer3', models.CharField(choices=[('Wz', 'Wangzi'), ('wz2', 'wangzi2')], max_length=30, verbose_name='reviewer3')),
                ('task', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='activflow.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('conclusion', models.CharField(choices=[('1', '通过'), ('2', '修改'), ('3', '拒绝')], max_length=30, verbose_name='终审')),
                ('task', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='activflow.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('result', models.CharField(choices=[('1', '通过'), ('2', '修改'), ('3', '拒绝')], max_length=30, verbose_name='初审')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='thesisReview.Review')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('subject', models.CharField(max_length=70, verbose_name='Subject')),
                ('thesis_title', models.CharField(max_length=200, verbose_name='论文题目')),
                ('content', models.TextField(max_length=1000, verbose_name='论文')),
                ('keywords', models.CharField(max_length=200, verbose_name='关键词')),
                ('abstract', models.TextField(max_length=200, verbose_name='概述')),
                ('task', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='activflow.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

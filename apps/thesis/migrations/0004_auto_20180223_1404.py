# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-02-23 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0003_auto_20180223_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='publish_time',
            field=models.DateField(null=True, verbose_name='发布时间'),
        ),
    ]

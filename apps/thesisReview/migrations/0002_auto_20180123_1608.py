# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-01-23 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesisReview', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

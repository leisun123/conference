# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-05 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('PaperReview', '0011_auto_20180306_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='id',
            field=models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paper',
            name='serial_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]

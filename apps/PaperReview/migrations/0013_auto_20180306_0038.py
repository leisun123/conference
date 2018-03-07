# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-05 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('PaperReview', '0012_auto_20180306_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='serial_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]

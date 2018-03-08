# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-05 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('PaperReview', '0010_auto_20180306_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='id',
        ),
        migrations.AddField(
            model_name='paper',
            name='serial_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

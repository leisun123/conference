# Generated by Django 2.0 on 2018-03-12 04:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaperReview', '0003_auto_20180311_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='file',
            field=models.FileField(max_length=51200, upload_to='thesis/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]

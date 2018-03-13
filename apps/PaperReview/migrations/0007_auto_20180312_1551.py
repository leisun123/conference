# Generated by Django 2.0.3 on 2018-03-12 07:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaperReview', '0006_auto_20180312_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='file',
            field=models.FileField(max_length=512000, upload_to='thesis/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]

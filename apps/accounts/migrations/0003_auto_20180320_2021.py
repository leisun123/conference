# Generated by Django 2.0.3 on 2018-03-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_scholar_is_assigned_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholar',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

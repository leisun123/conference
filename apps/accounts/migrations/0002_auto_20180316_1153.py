# Generated by Django 2.0.3 on 2018-03-16 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scholar',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='scholar',
            unique_together={('email',)},
        ),
    ]
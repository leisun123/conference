# Generated by Django 2.0 on 2018-03-07 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaperReview', '0020_auto_20180306_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='proposal_to_author',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
    ]
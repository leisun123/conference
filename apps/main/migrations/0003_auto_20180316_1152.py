# Generated by Django 2.0.3 on 2018-03-16 03:52

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180316_0050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sidebar',
            options={'ordering': ['rank'], 'verbose_name': 'SideBar Tag'},
        ),
        migrations.AlterField(
            model_name='generictagcontent',
            name='body',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='generictagcontent',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='parent_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.SideBar', verbose_name='parent node'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-25 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notespool', '0009_auto_20171024_2236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='date_created',
            new_name='created_on',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='student_created',
        ),
        migrations.AddField(
            model_name='comment',
            name='created_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='studynote',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='subpage',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='unit',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='created_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='studynote',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='subpage',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='unit',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

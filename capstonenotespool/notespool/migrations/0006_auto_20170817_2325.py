# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-17 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notespool', '0005_auto_20170816_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=15, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-24 07:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notespool', '0002_auto_20171024_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='studynotes',
            name='unit',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

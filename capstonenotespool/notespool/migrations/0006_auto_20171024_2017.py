# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-24 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notespool', '0005_studynotes_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studynotes',
            name='date_modified',
            field=models.DateField(),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-26 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notespool', '0013_subscriptions_unit_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]

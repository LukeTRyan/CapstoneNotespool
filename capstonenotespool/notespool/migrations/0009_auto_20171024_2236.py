# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-24 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notespool', '0008_auto_20171024_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='question',
            name='option1',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='question',
            name='option2',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='question',
            name='option3',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='question',
            name='option4',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='question',
            name='question',
            field=models.TextField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='notespool.Exam'),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]

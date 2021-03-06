# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-24 06:41
from __future__ import unicode_literals

import ckeditor.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, unique=True)),
                ('password', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=128, verbose_name="Answer's text")),
                ('related_quiz', models.IntegerField()),
                ('is_valid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('date_created', models.DateField(default=datetime.datetime.now)),
                ('date_modified', models.DateField(default=datetime.datetime.now)),
                ('student_created', models.IntegerField()),
                ('content', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('name', models.CharField(max_length=64, verbose_name='Exam name')),
                ('exam_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('unit', models.CharField(max_length=50, null=True)),
                ('slug', models.SlugField()),
                ('created_by', models.CharField(max_length=20, null=True)),
                ('created_on', models.DateField(default=datetime.datetime.now)),
                ('date_modified', models.DateField(default=datetime.datetime.now)),
                ('choices', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=256, verbose_name="Question's text")),
                ('related_quiz', models.IntegerField()),
                ('is_published', models.BooleanField(default=False)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='notespool.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, unique=True)),
                ('password', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('units', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=15, null=True)),
                ('last_name', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(max_length=40)),
                ('units_enrolled', models.IntegerField(null=True)),
                ('comments', models.CharField(max_length=100, null=True)),
                ('social', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudyNotes',
            fields=[
                ('notes_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=100)),
                ('created_by', models.IntegerField()),
                ('created_on', models.DateField(default=datetime.datetime.now)),
                ('content', ckeditor.fields.RichTextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('unit_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('unit_name', models.CharField(max_length=50, unique=True)),
                ('unit_code', models.CharField(max_length=50, unique=True)),
                ('staff', models.IntegerField(null=True)),
                ('students', models.IntegerField(null=True)),
                ('created_by', models.CharField(max_length=20)),
                ('created_on', models.DateField(default=datetime.datetime.now)),
                ('subpages', models.IntegerField(null=True)),
                ('notes', models.IntegerField(null=True)),
                ('approval', models.NullBooleanField(default=False)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnitSubpage',
            fields=[
                ('subpage_id', models.IntegerField(primary_key=True, serialize=False)),
                ('subpage_name', models.CharField(max_length=50, null=True)),
                ('unit', models.CharField(max_length=50, null=True)),
                ('studynotes', models.IntegerField(null=True)),
                ('created_by', models.CharField(max_length=20, null=True)),
                ('created_on', models.DateField(default=datetime.datetime.now)),
                ('approval', models.NullBooleanField(default=False)),
                ('images', models.ImageField(null=True, upload_to='')),
                ('quiz', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='notespool.Question'),
        ),
    ]

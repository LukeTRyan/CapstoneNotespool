from django.db import models
import datetime

class Admin(models.Model):
	admin_id = models.IntegerField(unique=True, primary_key=True)
	password = models.CharField(max_length=15, unique=True)

class Student(models.Model):
	student_id = models.IntegerField(unique=True, primary_key=True)
	password = models.CharField(max_length=15, unique=True)
	email = models.EmailField(max_length=40, unique=True)
	units_enrolled = models.IntegerField()
	comments = models.CharField(max_length=100)
	social = models.CharField(max_length=100)

class Unit(models.Model):
	unit_id = models.IntegerField(unique=True, primary_key=True)
	unit_name = models.CharField(max_length=50, unique=True)
	staff = models.IntegerField()
	students = models.IntegerField()
	created_by = models.IntegerField()
	created_on = models.DateField(default=datetime.datetime.now)
	subpages = models.IntegerField()
	notes = models.IntegerField()

class Staff(models.Model):
	staff_id = models.IntegerField(unique=True, primary_key=True)
	password = models.CharField(max_length=15, unique=True)
	email = models.EmailField(max_length=40, unique=True)
	units = models.IntegerField()

class UnitSubpage(models.Model):
	subpage_id = models.IntegerField(unique=True, primary_key=True)
	unit = models.IntegerField()
	studynotes = models.IntegerField()
	images = models.ImageField()
	quiz = models.CharField(max_length=100)


class Comment(models.Model):
	comment_id = models.IntegerField(unique=True, primary_key=True)
	date_created = models.DateField(default=datetime.datetime.now)
	date_modified = models.DateField(default=datetime.datetime.now)
	student_created = models.IntegerField()
	location = models.IntegerField()
	content = models.CharField(max_length=100)

class StudyNotes(models.Model):
	notes_id = models.IntegerField(unique=True, primary_key=True)
	type = models.CharField(max_length=100)
	created_by = models.IntegerField()
	created_on = models.DateField(default=datetime.datetime.now)
	location = models.IntegerField()




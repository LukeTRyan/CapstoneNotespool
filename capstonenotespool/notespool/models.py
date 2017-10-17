from django.db import models
import datetime
from django.utils.text import slugify
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField




#database model for admin
class Admin(models.Model):
	admin_id = models.IntegerField(unique=True, primary_key=True)
	username = models.CharField(max_length=50, unique=True, blank=True)
	password = models.CharField(max_length=15, unique=True)

#database model for students 
class Student(models.Model):
	student_id = models.IntegerField(unique=True, primary_key=True)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=15)
	first_name = models.CharField(max_length=15, null=True)
	last_name = models.CharField(max_length=15, null=True)
	email = models.EmailField(max_length=40)
	units_enrolled = models.IntegerField(null=True)
	comments = models.CharField(max_length=100, null=True)
	social = models.CharField(max_length=100, null=True)

def __str__(self):
	return self.username + ' - ' + self.password

class Unit(models.Model):
	unit_id = models.IntegerField(unique=True, primary_key=True)
	unit_name = models.CharField(max_length=50, unique=True)
	unit_code = models.CharField(max_length=50, unique=True)
	staff = models.IntegerField(null=True)
	students = models.IntegerField(null=True)
	created_by = models.CharField(max_length=20)
	created_on = models.DateField(default=datetime.datetime.now)
	subpages = models.IntegerField(null=True)
	notes = models.IntegerField(null=True)
	approval = models.NullBooleanField(default=False)
	slug = models.SlugField(unique=True, null=True)

def create_slug(instance, new_slug=None):
	slug = slugify(instance.unit_name)
	if new_slug is not None:
		slug = new_slug
	qs = Unit.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Unit)

#database model for staff 
class Staff(models.Model):
	staff_id = models.IntegerField(unique=True, primary_key=True)
	username = models.CharField(max_length=50, unique=True, blank=True)
	password = models.CharField(max_length=15, unique=True)
	email = models.EmailField(max_length=40, unique=True)
	units = models.IntegerField()

class UnitSubpage(models.Model):
	subpage_id = models.IntegerField(primary_key=True)
	subpage_name = models.CharField(max_length=50, null=True)
	unit = models.CharField(max_length=50, null=True)
	studynotes = models.IntegerField(null=True)
	created_by = models.CharField(max_length=20, null=True)
	created_on = models.DateField(default=datetime.datetime.now)
	approval = models.NullBooleanField(default=False)
	images = models.ImageField(null=True)
	quiz = models.CharField(max_length=100, null=True)


class Comment(models.Model):
	comment_id = models.IntegerField(unique=True, primary_key=True)
	date_created = models.DateField(default=datetime.datetime.now)
	date_modified = models.DateField(default=datetime.datetime.now)
	student_created = models.IntegerField()
	content = models.CharField(max_length=100)

class StudyNotes(models.Model):
	notes_id = models.IntegerField(unique=True, primary_key=True)
	type = models.CharField(max_length=100)
	created_by = models.IntegerField()
	created_on = models.DateField(default=datetime.datetime.now)
	content = RichTextField(null=True)

class Document(models.Model):
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class Exam(models.Model):
	"""
	Exam's model, works as a wrapper for the questions
	"""
	name = models.CharField(max_length=64, verbose_name=u'Exam name', )
	exam_id = models.IntegerField(unique=True, primary_key=True)
	unit = models.CharField(max_length=50, null=True)
	slug = models.SlugField()
	created_by = models.CharField(max_length=20, null=True)
	created_on = models.DateField(default=datetime.datetime.now)
	date_modified = models.DateField(default=datetime.datetime.now)
	choices = models.IntegerField(null=True)

	def __str__(self):
		return self.name

def create_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Exam.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Exam)

	

class Question(models.Model):
	question_text = models.CharField(max_length=256, verbose_name=u'Question\'s text')
	related_quiz = models.IntegerField()
	is_published = models.BooleanField(default=False)
	exam = models.ForeignKey(Exam, related_name='questions')

	def __str__(self):
		return "{content} - {published}".format(content=self.question_text, published=self.is_published)


class Answer(models.Model):
	"""
	Answer's Model, which is used as the answer in Question Model
	"""
	text = models.CharField(max_length=128, verbose_name=u'Answer\'s text')
	related_quiz = models.IntegerField()
	is_valid = models.BooleanField(default=False)
	question = models.ForeignKey(Question, related_name='answers')

	def __str__(self):
		return self.text


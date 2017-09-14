from django.db import models
import datetime

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
	location = models.IntegerField()
	content = models.CharField(max_length=100)

class StudyNotes(models.Model):
	notes_id = models.IntegerField(unique=True, primary_key=True)
	type = models.CharField(max_length=100)
	created_by = models.IntegerField()
	created_on = models.DateField(default=datetime.datetime.now)
	location = models.IntegerField()

class Document(models.Model):
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class Exam(models.Model):
	"""
	Exam's model, works as a wrapper for the questions
	"""
	name = models.CharField(max_length=64, verbose_name=u'Exam name', )
	slug = models.SlugField()

	def __str__(self):
		return self.name


class Question(models.Model):
	question_text = models.CharField(max_length=256, verbose_name=u'Question\'s text')
	is_published = models.BooleanField(default=False)
	exam = models.ForeignKey(Exam, related_name='questions')

	def __str__(self):
		return "{content} - {published}".format(content=self.question_text, published=self.is_published)


class Answer(models.Model):
	"""
	Answer's Model, which is used as the answer in Question Model
	"""
	text = models.CharField(max_length=128, verbose_name=u'Answer\'s text')
	is_valid = models.BooleanField(default=False)
	question = models.ForeignKey(Question, related_name='answers')

	def __str__(self):
		return self.text

class Event(models.Model):
	title = models.CharField(max_length=255)
	date = models.DateField()
	is_outdoors = models.BooleanField()

	#index = djangosearch.ModelIndex(text=['title'], 
	#additional=['date', 'is_outdoors'])

# run a search
#results = Event.index.search("django conference")




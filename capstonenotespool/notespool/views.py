from django.shortcuts import render, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Student, Document, Unit, UnitSubpage, Exam, Question, Answer
from .forms import LoginForm, RegistrationForm, DeleteAccountForm, EditAccountForm, PasswordResetForm, CreateAccountForm, DocumentForm, CreateUnitForm, EditUnitForm, CreateSubpageForm, CreateQuizForm, EditQuizForm
from django.contrib.auth import authenticate,get_user_model,login,logout
from django import forms
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from .functions import password_verification, email_verification, id_generator
from xml.dom import minidom
from django.db.models import Count, Q
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import get_object_or_404
from django.shortcuts import *
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
from django.core.urlresolvers import reverse

fromaddr='LukeTRyan95@gmail.com'
username='LukeTRyan95@gmail.com'
password='Uberhaxor123'

#from calendar import HTMLCalendar
#from datetime import date
#from itertools import groupby

#from django.utils.html import conditional_escape as esc

#class UpcomingAssessment(HTMLCalendar):

#	def __init__(self, assessments):
#		super(UpcomingAssessment, self).__init__()
#		self.assessments = self.group_by_day(assessments)

#	def formatday(self, day, weekday):
#		if day != 0:
#			cssclass = self.cssclasses[weekday]
#			if date.today() == date(self.year, self.month, day):
#				cssclass += ' today'
#			if day in self.assessments:
#				cssclass += ' filled'
#				body = ['<ul>']
#	for assessment in self.assessments[day]:
#		body.append('')
#	<li>
#       body.append('<a href="%s">' % assessment.get_absolute_url())
#          body.append(esc(assessment.title))
#            body.append('')
#       </a>
#    </li>
#    body.append('')
#</ul>
#                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
#           return self.day_cell(cssclass, day)
#        return self.day_cell('noday', '&nbsp;')

 #   def formatmonth(self, year, month):
 #       self.year, self.month = year, month
 #       return super(UpcomingAssessment, self).formatmonth(year, month)

#    def group_by_day(self, assessments):
#        field = lambda assessment: assessment.performed_at.day
#        return dict(
#            [(day, list(items)) for day, items in groupby(assessments, field)]
#        )

#    def day_cell(self, cssclass, body):
#        return '<td class="%s">%s</td>' % (cssclass, body)

#home
def index(request):
	if 'redirect' in request.session and request.session['redirect'] == "Login":
		message = "Logged in successfully"
		username = request.session['user_id']
		request.session['redirect'] = None
		return render(request, "index.html", {'userp': username, 'message': message})
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('index.html', {'userp': username})
	return render(request, 'index.html', {})
	
#logs in user
def loginuser(request):
	form = LoginForm(request.POST or None)
	if 'redirect' in request.session and request.session['redirect'] == "LoginRequired":
		message = "Please login to continue"
		request.session['redirect'] = None
		return render(request, "login.html", {'form': form, 'message': message})
    
	if 'user_id' in request.session and request.session['user_id'] is not None:
		return HttpResponseRedirect('/')

	if form.is_valid():
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]
		user = authenticate(username=username, password=password)
		if user is not None:
				if user.is_active == True:
					login(request,user)
					request.session['user_id'] = username
					request.session['redirect'] = "Login"
					return HttpResponseRedirect('/')
				else:
					message = "Error"
					return render(request, "registration_form.html", {'form': form, 'message': message})
		else:
			return render(request,'registration_form.html', {'errormessage':'Invalid login'})
	else:
		return render(request, 'login.html', {'form': form})

#Creates user account
def registeraccount(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		request.session['redirect'] = "AlreadyLogged"                    
		return HttpResponseRedirect('/')

	form = RegistrationForm(data=request.POST)
	if form.is_valid():
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]
		password2 = form.cleaned_data["password2"]
		email = form.cleaned_data["email"]
		if User.objects.filter(username = username).exists():  #username verification
			message = "Username already exists please try again"
			return render(request, "registration_form.html", {'form': form, 'message': message})
		if password != password2:  #password match verification
			message = "Passwords do not match please try again"
			return render(request, "registration_form.html", {'form': form, 'message': message})
		if (password_verification(password)) == False:   #password strength verification
			message = "Password is not strong enough"
			return render(request, "registration_form.html", {'form': form, 'message': message})
		if email and User.objects.filter(email=email).exclude(username=username).count():   #email match verification
			message = "Email already exists"
			return render(request, "registration_form.html", {'form': form, 'message': message})
		#if (email_verification(email)) == False:
		#	message = "Email is not valid QUT email"
		#	return render(request, "registration_form.html", {'form': form, 'message': message})
		else:
			user = User.objects.create_user(username=username,password=password,email=email)
			newUserModel = Student(student_id = user.id,
									username = username,
									password = password,
									email = email)
			newUserModel.save()
			if user.check_password(password):
				user = authenticate(username=username, password=password)
				user.is_active=False
				user.save()
				id=user.id
				email=user.email
				send_email(email,id)
				message = "Activation Email Sent"
				return render(request, 'registration_form.html', {'form' : form, 'message': message})
	else:
		return render(request, 'registration_form.html', {'form' : form})

#activates user accounts
def activate(request):
	id=int(request.GET.get('id'))
	user = User.objects.get(id=id)
	user.is_active=True
	user.save()
	request.session['redirect'] = "NewAccount"  
	return render_to_response('activation.html')

#deletes the user account for password reset
def activatereset(request):
	id=int(request.GET.get('id'))
	user = User.objects.get(id=id)
	deleteUser = Student.objects.get(student_id = user.id)
	deleteUser.delete()
	user.delete()
	user.is_active=False
	request.session['user_id'] = None
	request.session['redirect'] = "activatereset"  
	return render_to_response('activatereset.html')
	
#sends verification email to the user 
def send_email(toaddr,id):
	text = "Hi!\nHow are you?\nHere is the link to activate your account:\nhttps://capstonenotespool.herokuapp.com/activation/?id=%s" %(id)
	part1 = MIMEText(text, 'plain')
	msg = MIMEMultipart('alternative')
	msg.attach(part1)
	subject="Activate your account at Capstone Notespool"
	msg="""\From: %s\nTo: %s\nSubject: %s\n\n%s""" %(fromaddr,toaddr,subject,msg.as_string())
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr,[toaddr],msg)
	server.quit()

#sends verification email to the user to reset the account 
def send_reset_email(toaddr,id):
	text = "Hi!\nHow are you?\nHere is the link to reset your password:\nhttp://127.0.0.1:8000/activatereset/?id=%s" %(id)
	part1 = MIMEText(text, 'plain')
	msg = MIMEMultipart('alternative')
	msg.attach(part1)
	subject="Reset your password at Capstone Notespool"
	msg="""\From: %s\nTo: %s\nSubject: %s\n\n%s""" %(fromaddr,toaddr,subject,msg.as_string())
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr,[toaddr],msg)
	server.quit()

#form to send the user a password reset email
def passwordreset(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		return HttpResponseRedirect('/')

	form = PasswordResetForm(data=request.POST)
	if form.is_valid():
		email = form.cleaned_data["email"]
		if email and User.objects.filter(email=email).exclude(username=username).count():   #email match verification
			user = User.objects.get(email = email)
			id=user.id
			email=user.email
			send_reset_email(email,id)
			message = "Reset Email Sent"
			return render(request, 'password_change_form.html', {'form' : form, 'message': message})
		else:
			message = "Account associated with that email does not exist"
			return render(request, 'password_change_form.html', {'form' : form, 'message': message})
	return render(request, 'password_change_form.html', {'form' : form})

#logs out the user
def logout(request):
	django_logout(request)
	return HttpResponseRedirect('/')
	
#Site privacy policy
def privacypolicy(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('privacypolicy.html', {'userp': username})
	return render_to_response('privacypolicy.html')

#User agreement/terms of use
def useragreement(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('useragreement.html', {'userp': username})
	return render_to_response('useragreement.html')

#Site owners background
def aboutus(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('aboutus.html', {'userp': username})
	return render_to_response('aboutus.html')
   
#Site owners contact information
def contact(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('contact.html', {'userp': username})
	return render_to_response('contact.html')

#Notespool homepage
def notespool(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		units = Unit.objects.all()
		return render_to_response('notespool.html', {'userp': username, 'units':units})
	else:
		return HttpResponseRedirect('/')
	return render_to_response('notespool.html', {'userp': username})

def unit_page(request,unitname):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		unit = Unit.objects.get(slug = unitname)
		unitName = unit.unit_name
		unitSLUG = unit.slug

		subpages = UnitSubpage.objects.filter(unit = unitName)
		return render_to_response('unit_page.html', {'userp': username, 'unitName':unitName, 'subpages':subpages, 'unitSLUG':unitSLUG})
	else:
		return HttpResponseRedirect('/')
	return render_to_response('unit_page.html', {'userp': username})

def unit_subpage(request,unitname,subpagename):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		unit = Unit.objects.get(slug = unitname)
		unitName = unit.unit_name
		unitSLUG = unit.slug
		quizzes = Exam.objects.all()
		questions = Question.objects.all()
		answers = Answer.objects.all()
		print(quizzes)
		print(questions)
		print(answers)

		return render_to_response('unit_subpage.html', {'userp': username, 'unitName':unitName, 'subpageNAME':subpagename, 'unitSLUG':unitSLUG, 'quizzes':quizzes})
	else:
		return HttpResponseRedirect('/')
	return render_to_response('unit_subpage.html', {'userp': username})

def create_quiz(request,unitname,subpagename):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		unit = Unit.objects.get(slug = unitname)

		if request.method == 'GET':
			request.session['previous_url'] = request.META.get('HTTP_REFERER')

		form = CreateQuizForm(request.POST or None)

		if form.is_valid():
			quiz_name = form.cleaned_data['quiz_name']
			if Exam.objects.filter(name = quiz_name).exists() and Exam.objects.filter(unit = unit.unit_name):
				message = "Quiz already exists"
				return render(request,'create_quiz.html', {'userp': username, 'unit': unit, 'form': form, 'message': message, 'subpagename':subpagename})
			else:

				try: 
					get_latest = Exam.objects.latest('exam_id')
					latest_id = get_latest.exam_id
				except ObjectDoesNotExist:
					latest_id = 0

				newquiz = Exam(exam_id = latest_id + 1, name = quiz_name, unit = unit.unit_name, created_by = username)
				newquiz.save()
				return HttpResponseRedirect(request.session['previous_url'])
	else:
		return HttpResponseRedirect('/login')
	return render_to_response('create_quiz.html', {'userp': username, 'form':form, 'unit':unit, 'subpagename':subpagename})


def edit_quiz(request,unitname,subpagename,quizname):
	examInstance = Exam.objects.get(slug = quizname)
	unit = Unit.objects.get(slug = unitname)
	createdBy = examInstance.created_by
	if 'user_id' not in request.session or request.session['user_id'] != "admin" or request.session['user_id'] != createdBy:
		return HttpResponseRedirect('/')
	username = request.session['user_id']

	if request.method == 'GET':
			request.session['previous_url'] = request.META.get('HTTP_REFERER')

	questions = Question.objects.all()
	answers = Answer.objects.all()

	form = EditQuizForm(request.POST or None)
	if form.is_valid():
		question_text = form.cleaned_data['question_text']
		answer_text = form.cleaned_data['answer_text']

		try: 
			get_latestq = Question.objects.latest('id')
			latest_idq = get_latestq.id
			get_latesta = Answer.objects.latest('id')
			latest_ida = get_latesta.id
		except ObjectDoesNotExist:
			latest_idq = 0
			latest_ida = 0
		
		newQuestion = Question(question_text = question_text, exam = examInstance, related_quiz = examInstance.exam_id, id = latest_idq + 1, is_published = True)
		newQuestion.save()	
		newAnswer = Answer(text = answer_text, question = newQuestion, related_quiz = examInstance.exam_id, id = latest_ida + 1)
		newAnswer.save()
		return HttpResponseRedirect(request.session['previous_url'])

	return render_to_response('edit_quiz.html', {'userp': username, 'exam': examInstance, 'form':form, 'subpagename':subpagename, 'unit':unit, 'questions':questions, 'answers':answers })


def delete_quiz(request,unitname,examid):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	quizzes = Exam.objects.all()
	deletequiz = Exam.objects.get(exam_id = examid, unit = unitname)
	deletequiz.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#function index to view, edit, create and delete users 
def administrator(request):
        if 'user_id' not in request.session or request.session['user_id'] != "admin":
                return HttpResponseRedirect('/')

        username = request.session['user_id']
        users = User.objects.all()
        query = request.GET.get("q")
        if query:
                users = users.filter(
                        Q(username__icontains=query)|
                        Q(id__icontains=query)|
                        Q(first_name__icontains=query)|
                        Q(last_name__icontains=query)|
                        Q(email__icontains=query)
                        ).distinct()
        return render_to_response('administrator.html', {'userp': username,'users': users})

#admin function to view units
def view_unit(request):
		if 'user_id' not in request.session or request.session['user_id'] != "admin":
			return HttpResponseRedirect('/')
	
		username = request.session['user_id']
		units = Unit.objects.all()
		query = request.GET.get("q")
		if query:
				units = units.filter(
						Q(unit_name__icontains=query)|
						Q(unit_id__icontains=query)|
						Q(unit_code__icontains=query)
						).distinct()
	
	
		return render_to_response('view_units.html', {'userp': username,'units': units})

def view_subpages(request):
        if 'user_id' not in request.session or request.session['user_id'] != "admin":
                return HttpResponseRedirect('/')

        username = request.session['user_id']
        subpages = UnitSubpage.objects.all()
        query = request.GET.get("q")
        if query:
                subpages = subpages.filter(
                        Q(subpage_id__icontains=query)|
                        Q(subpage_name__icontains=query)|
                        Q(unit__icontains=query)
                        ).distinct()
	
        return render_to_response('view_subpages.html', {'userp': username,'subpages': subpages})

#function to create units 
def create_unit(request):
	if request.session['user_id'] is None:
		return HttpResponseRedirect('/login')
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']

	try: 
		get_latest = Unit.objects.latest('unit_id')
		latest_id = get_latest.unit_id
	except ObjectDoesNotExist:
		latest_id = 0


	form = CreateUnitForm(request.POST or None)
		
	if form.is_valid():
		unit_name = form.cleaned_data['unit_name']
		unit_code = form.cleaned_data['unit_code']

		if Unit.objects.filter(unit_name = unit_name).exists():
			username = request.session['user_id']
			message = "Unit already exists"
			return render(request,'create_unit.html', {'userp': username, 'form': form, 'message': message})

		if Unit.objects.filter(unit_code = unit_code).exists():
			username = request.session['user_id']
			message = "Unit already exists"
			return render(request,'create_unit.html', {'userp': username, 'form': form, 'message': message})
		else:
			newUnit = Unit(unit_id = latest_id + 1, unit_name = unit_name, unit_code = unit_code, created_by = username)
			newUnit.save()

			AssessmentSubpage = UnitSubpage(subpage_id = id_generator(), subpage_name = "Assessment", unit = newUnit.unit_name, created_by = username, approval = True)
			AssessmentSubpage.save()

			QuizSubpage = UnitSubpage(subpage_id = id_generator(), subpage_name = "Quizzes", unit = newUnit.unit_name, created_by = username, approval = True)
			QuizSubpage.save()

			LectureSubpage = UnitSubpage(subpage_id = id_generator(), subpage_name = "Lectures", unit = newUnit.unit_name, created_by = username,  approval = True)
			LectureSubpage.save()

			TutorialSubpage = UnitSubpage(subpage_id = id_generator(), subpage_name = "Tutorials", unit = newUnit.unit_name, created_by = username,  approval = True)
			TutorialSubpage.save()
			

			request.session['redirect'] = "Unit_created"
			return HttpResponseRedirect('/notespool')
	else:
		return render(request, 'create_unit.html', {'userp':username, 'form':form}) 

def create_subpage(request,unitname):
	if request.session['user_id'] is None:
		return HttpResponseRedirect('/login')
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']

	unitDetails = Unit.objects.get(slug = unitname)

	form = CreateSubpageForm(request.POST or None)
		
	if form.is_valid():
		subpage_name = form.cleaned_data['subpage_name']

		if UnitSubpage.objects.filter(subpage_name = subpage_name).exists():
			username = request.session['user_id']
			message = "subpage already exists"
			return render(request,'create_subpage.html', {'userp': username,'sent_unit': unitDetails, 'form': form, 'message': message})

		else:
			newSubpage = UnitSubpage(subpage_id = id_generator(), subpage_name = subpage_name, unit = unitDetails.unit_name, created_by = username)
			newSubpage.save()

			request.session['redirect'] = "subpage_created"
			return HttpResponseRedirect('/notespool')
	else:
		return render(request, 'create_subpage.html', {'userp':username, 'sent_unit': unitDetails, 'form':form}) 

#admin function to delete units
def delete_unit(request,unitid):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	units = Unit.objects.all()
	deleteUnit = Unit.objects.get(unit_id = unitid)
	deleteUnit.delete()

	subpages = UnitSubpage.objects.all()
	UnitSubpage.objects.filter(unit = deleteUnit.unit_name).delete()
	return render_to_response('view_units.html', {'userp': username, 'units': units})

def delete_subpage(request,subpageid):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	subpages = UnitSubpage.objects.all()
	deletesubpage = UnitSubpage.objects.get(subpage_id = subpageid)
	deletesubpage.delete()
	return render_to_response('view_subpages.html', {'userp': username, 'subpages': subpages})

#admin function to edit units
def edit_unit(request,unitid):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	unitDetails = Unit.objects.get(unit_id = unitid)
	form = EditUnitForm(request.POST or None)
	data = {'unit_name': unitDetails.unit_name,
            'unit_code': unitDetails.unit_code,
            'approval': unitDetails.approval}

	if form.is_valid():
		unit_name = form.cleaned_data['unit_name']
		unit_code = form.cleaned_data['unit_code']
		approval = form.cleaned_data['approval']

	
		if Unit.objects.filter(unit_name = unit_name).exists() and (unit_name != unitDetails.unit_name):
			username = request.session['user_id']
			message = "Unit name already exists"
			return render(request,'edit_unit.html', {'userp': username,'sent_unit': unitDetails, 'form': form, 'message': message})

		if Unit.objects.filter(unit_code = unit_code).exists() and (unit_code != unitDetails.unit_code):
			username = request.session['user_id']
			message = "Unit code already exists"
			return render(request,'edit_unit.html', {'userp': username,'sent_unit': unitDetails, 'form': form, 'message': message})

		unitDetails.unit_name = unit_name
		unitDetails.unit_code = unit_code
		unitDetails.approval = approval
		unitDetails.save()

		request.session['redirect'] = "Unit_edited"
		return HttpResponseRedirect('/view_unit/')
	
	form = EditUnitForm(request.POST or None, initial=data) 
	return render(request, 'edit_unit.html', {'userp': username,'sent_unit': unitDetails, 'form': form})

#admin function to approve the unit once it has been created
def approve_unit(request,unitid):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	units = Unit.objects.all()
	approveUnit = Unit.objects.get(unit_id = unitid)
	approveUnit.approval = True
	approveUnit.save()
	return render_to_response('view_units.html', {'userp': username, 'units': units})

def approve_subpage(request,subpageid):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	subpages = UnitSubpage.objects.all()
	approvesubpage = UnitSubpage.objects.get(subpage_id = subpageid)
	approvesubpage.approval = True
	approvesubpage.save()
	return render_to_response('view_subpages.html', {'userp': username, 'subpages': subpages})

#admin function to edit user details 
def editAccount(request, account):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	userProfile = User.objects.get(username = account)
	form = EditAccountForm(request.POST or None)
	data = {'username': userProfile.username,
			'password': userProfile.password,
            'first_name': userProfile.first_name,
            'last_name': userProfile.last_name,
            'email': userProfile.email}

	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']
		email = form.cleaned_data['email']
		
		if User.objects.filter(username = username).exists() and (username != account):
			username = request.session['user_id']
			message = "Username already exists"
			return render(request,'edit_account.html', {'userp': username,'sent_user': userProfile, 'form': form, 'message': message})

		if User.objects.filter(email = email).exists() and (email != userProfile.email):
			username = request.session['user_id']
			message = "Email already exists"
			return render(request,'edit_account.html', {'userp': username,'sent_user': userProfile, 'form': form, 'message': message})

		userProfile.username = username
		userProfile.password = password
		userProfile.first_name = first_name
		userProfile.last_name = last_name
		userProfile.email = email
		userProfile.save()

		student = Student.objects.get(username = account)
		student.username = username
		student.password = password
		student.first_name = first_name
		student.last_name = last_name
		student.email = email
		student.save()

		request.session['redirect'] = "User_edited"
		return HttpResponseRedirect('/administrator')
		
	form = EditAccountForm(request.POST or None, initial=data) 
	return render(request, 'edit_account.html', {'userp': username,'sent_user': userProfile, 'form': form})
	
#admin function to delete existing accounts
def deleteAccount(request, account):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	users = User.objects.all()
	username = request.session['user_id']
	deleteUser = User.objects.get(username = account)
	deleteUser.delete()
	deleteStudent = Student.objects.get(username = account)
	deleteStudent.delete()
	return render_to_response('administrator.html', {'userp': username, 'users': users})

#admin function to create accounts
def createAccount(request):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']

	form = CreateAccountForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']
		email = form.cleaned_data['email']
	
		if User.objects.filter(username = username).exists():
			username = request.session['user_id']
			message = "Username already exists"
			return render(request,'create_account.html', {'userp': username, 'form': form, 'message': message})
		if User.objects.filter(email = email).exists():
			username = request.session['user_id']
			message = "Email already exists"
			return render(request,'create_account.html', {'userp': username, 'form': form, 'message': message})
		else:
			user = User.objects.create_user(username=username,password=password,email=email,first_name = first_name,last_name = last_name)
			user.save()
			newUserModel = Student(student_id = user.id,
									username = username,
									password = password,
									email = email,
									first_name = first_name,
									last_name = last_name)
			newUserModel.save()
			request.session['redirect'] = "User_created"
			return HttpResponseRedirect('/administrator')
	else:
		return render(request,'create_account.html', {'userp': username, 'form': form})

#user account - users can edit and delete their accounts from here
def account(request):
	if request.session['user_id'] is None:
		return HttpResponseRedirect('/login')
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']

	form = DeleteAccountForm(request.POST)
	if form.is_valid():
		username = request.session['user_id']
		password = form.cleaned_data['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			deleteUser = Student.objects.get(username = username)
			deleteUser.delete()
			user.delete()
			user.is_active=False
			request.session['user_id'] = None
			return HttpResponseRedirect('/')
		else:
			message = "Incorrect credentials"
			return render(request, "account.html", {'form': form, 'message': message, 'userp': username})
	return render(request, "account.html", {'form': form, 'userp': username})

#list of uploaded documents - currently limited to admin
def list(request):
        if 'user_id' not in request.session or request.session['user_id'] != "admin":
                return HttpResponseRedirect('/')

        username = request.session['user_id']
        # Handle file upload
        if request.method == 'POST':
                form = DocumentForm(request.POST, request.FILES)
                if form.is_valid():
                        newdoc = Document(docfile = request.FILES['docfile'])
                        newdoc.save()
 
                        # Redirect to the document list after POST
                        return HttpResponseRedirect('/list')
        else:
                form = DocumentForm() # A empty, unbound form
 
        # Load documents for the list page
        documents = Document.objects.all()
        query = request.GET.get("q")
        if query:
                documents = documents.filter(
                        Q(pk__icontains=query)|
                        Q(docfile__icontains=query)
                        ).distinct()
	
 
        # Render list page with the documents and the form
        return render(request, 'list.html',
                {'documents': documents, 'form': form, 'userp':username}) 

def delete_document(request,documentpk):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	documents = Document.objects.all()
	for document in documents:
		if Document.objects.get(pk = documentpk):
			document.docfile.delete()
			document.delete()
			return HttpResponseRedirect('/list')
	return render_to_response('list.html', {'userp': username, 'documents': documents})

#report content		
def report(request):		
	if request.session['user_id'] is None:		
		return HttpResponseRedirect('/login')		
	if 'user_id' in request.session and request.session['user_id'] is not None:		
		username = request.session['user_id']		
		
	form = ReportContent(request.POST)		
	if form.is_valid():		
		username = request.session['user_id']		
		password = form.cleaned_data['password']		
		user = authenticate(username = username, password = password)		
		if user is not None:		
			deleteDocument = Student.objects.get(username = username)		
			deleteDocument.delete()		
			user.delete()		
			user.is_active=False		
			request.session['user_id'] = None		
			return HttpResponseRedirect('/')		
		else:		
			message = "Content Removed"		
			return render(request, "account.html", {'form': form, 'message': message, 'userp': username})		
	return render(request, "account.html", {'form': form, 'userp': username})
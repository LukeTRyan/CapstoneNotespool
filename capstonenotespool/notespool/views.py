from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Student, Document, Unit
from .forms import LoginForm, RegistrationForm, DeleteAccountForm, EditAccountForm, PasswordResetForm, CreateAccountForm, DocumentForm, CreateUnitForm, EditUnitForm
from django.contrib.auth import authenticate,get_user_model,login,logout
from django import forms
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from .functions import password_verification, email_verification, id_generator
from xml.dom import minidom
from django.db.models import Count
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
from django.core.urlresolvers import reverse

fromaddr='LukeTRyan95@gmail.com'
username='LukeTRyan95@gmail.com'
password='Uberhaxor123'


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
	text = "Hi!\nHow are you?\nHere is the link to activate your account:\nhttp://127.0.0.1:8000/activation/?id=%s" %(id)
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
                unit = Unit.objects.get(unit_name = unitname)
                unitName = unit.unit_name
                return render_to_response('unit_page.html', {'userp': username, 'unitName':unitName})
        else:
                return HttpResponseRedirect('/')
        return render_to_response('unit_page.html', {'userp': username})




#function index to view, edit, create and delete users 
def administrator(request):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	users = User.objects.all()
	return render_to_response('administrator.html', {'userp': username,'users': users})

#admin function to view units
def view_unit(request):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	units = Unit.objects.all()
	return render_to_response('view_units.html', {'userp': username,'units': units})

#function to create units 
def create_unit(request):
	if request.session['user_id'] is None:
		return HttpResponseRedirect('/login')
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']

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
			newUnit = Unit(unit_id = id_generator(), unit_name = unit_name, unit_code = unit_code, created_by = username)
			newUnit.save()
			request.session['redirect'] = "Unit_created"
			return HttpResponseRedirect('/notespool')
	else:
		return render(request, 'create_unit.html', {'userp':username, 'form':form}) 

#admin function to delete units
def delete_unit(request,unitid):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	units = Unit.objects.all()
	deleteUnit = Unit.objects.get(unit_id = unitid)
	deleteUnit.delete()
	return render_to_response('view_units.html', {'userp': username, 'units': units})

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
 
    # Render list page with the documents and the form
	return render(request, 'list.html',
		{'documents': documents, 'form': form, 'userp':username}) 


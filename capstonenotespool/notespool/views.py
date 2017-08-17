from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import LoginForm, RegistrationForm, DeleteAccountForm, EditAccountForm, PasswordResetForm, CreateAccountForm
from django.contrib.auth import authenticate,get_user_model,login,logout
from django import forms
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from .functions import password_verification, email_verification
from xml.dom import minidom
from django.db.models import Count
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import get_object_or_404

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
	return render_to_response('index.html')
	

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


def activate(request):
	id=int(request.GET.get('id'))
	user = User.objects.get(id=id)
	user.is_active=True
	user.save()
	request.session['redirect'] = "NewAccount"  
	return render_to_response('activation.html')

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
	else:
		return render(request, 'password_change_form.html', {'form' : form, 'message': message})

#logs out the user
def logout(request):
	if request.session['user_id'] is None:
		return HttpResponseRedirect('/login')

	username = request.session['user_id']
	user = User.objects.get(username = username)
	[s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
	request.session['user_id'] = None
	request.session['redirect'] = "Logout"
	return HttpResponseRedirect('/')



def privacypolicy(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('privacypolicy.html', {'userp': username})
	return render_to_response('privacypolicy.html')

def useragreement(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('useragreement.html', {'userp': username})
	return render_to_response('useragreement.html')

def aboutus(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('aboutus.html', {'userp': username})
	return render_to_response('aboutus.html')
    
def contact(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('contact.html', {'userp': username})
	return render_to_response('contact.html')

def notespool(request):
	if 'user_id' in request.session and request.session['user_id'] is not None:
		username = request.session['user_id']
		return render_to_response('notespool.html', {'userp': username})
	return render_to_response('notespool.html')

	



#function index to view, edit, create and delete users 
def administrator(request):
	if 'user_id' not in request.session or request.session['user_id'] != "admin":
		return HttpResponseRedirect('/')

	username = request.session['user_id']
	users = User.objects.all()
	return render_to_response('administrator.html', {'userp': username,'users': users})

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

		if username == account or User.objects.filter(username = username).exists() == False:
			user = User.objects.get(username = account)
			user.username = username
			user.password = password
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.save()

			student = Student.objects.get(username = account)
			student.username = username
			student.password = password
			student.first_name = first_name
			student.last_name = last_name
			student.email = email
			student.save()

			request.session['redirect'] = "User_edited"
			return HttpResponseRedirect('/administrator')
		else:
			message = "Username not valid"
			form = EditAccountForm(initial=data)  
			return render(request, 'edit_account.html', {'userp': username, 'message': message, 'sent_user': userProfile, 'form': form})
	form = EditAccountForm(request.POST or None, initial=data) 
	return render(request, 'edit_account.html', {'userp': username,'sent_user': userProfile, 'form': form})
	

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
	
		if User.objects.filter(username = username).exists() == False and User.objects.filter(email = email).exists() == False:
			user = User.objects.create_user(username=username,password=password,email=email, first_name = first_name, last_name = last_name)
			newUserModel = Student(student_id = user.id,
									username = username,
									password = password,
									email = email)
			newUserModel.save()
			user.save()
			request.session['redirect'] = "User_created"
			return HttpResponseRedirect('/administrator')
	return render(request,'create_account.html', {'userp': username, 'form': form})




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

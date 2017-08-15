from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, DeleteAccountForm
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
    
	if 'redirect' in request.session and request.session['redirect'] == "NewAccount":
		message = "Account Created"
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
def createaccount(request):
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
			user = User.objects.create_user(username=username, password=password, email=email)
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



def passwordreset(request):
	return render(request, 'password_change_form.html', {})

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
			deleteUser = User.objects.get(username = username)
			deleteUser.delete()
			user.delete()
			user.is_active=False
			request.session['user_id'] = None
			return HttpResponseRedirect('/')
		else:
			message = "Incorrect credentials"
			return render(request, "account.html", {'form': form, 'message': message, 'userp': username})
	return render(request, "account.html", {'form': form, 'userp': username})
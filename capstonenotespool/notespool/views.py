from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate,get_user_model,login,logout

def index(request):
    return render(request, 'index.html', {})

def login(request):
	print(request.user.is_authenticated())
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]
		user = authenticate(username=username, password=password)
		if user is not None:
				if user.is_active:											
					login(request,user)
					return redirect('register_activate:main')
				else:
					message = "Error"
					return render(request, "registration_form.html", {'form': form, 'message': message})
		else:
			return render(request,'registration_form.html',{'errormessage':'Invalid login'})

	return render(request, 'login.html', {'form': form})


def createaccount(request):
	form = RegistrationForm(request.POST)
	if form.is_valid():
		username=request.POST['username']
		password=request.POST['password']
		password2=request.POST['password2']
		email=request.POST['email']
		user=authenticate(username=username,password=password)
		user.is_active=False
		user.save()
		return HttpResponseRedirect('/login')
		#id=user.id
		#email=user.email
	else:
		return render(request, 'registration_form.html', {})

def passwordreset(request):
	return render(request, 'password_change_form.html', {})

def privacypolicy(request):
	return render(request, 'privacypolicy.html', {})

def useragreement(request):
	return render(request, 'useragreement.html', {})

def aboutus(request):
    return render(request, 'aboutus.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def notespool(request):
    return render(request, 'notespool.html', {})




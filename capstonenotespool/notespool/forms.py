from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.contrib.auth.models import User

#login form for user login
class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("User does not exist.")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("User is no longer active.")
		return super(LoginForm, self).clean(*args, **kwargs)


#registration form for users
class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=15);
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	email = forms.EmailField(widget=forms.EmailInput)

class DeleteAccountForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput)

class EditAccountForm(forms.Form):
    GENDER_CHOICES=[('M', 'M'), ('F', 'F')]
    
    username = forms.CharField()
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    DOB = forms.DateField(widget=forms.DateInput)
    email = forms.EmailField(widget=forms.EmailInput)
   
class PasswordResetForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput)
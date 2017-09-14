from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

#login form for user login
class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	captcha = CaptchaField()

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
	username = forms.CharField(max_length=15)
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	email = forms.EmailField(widget=forms.EmailInput)

class DeleteAccountForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput)

class EditAccountForm(forms.Form):
	username = forms.CharField(max_length=15)
	password = forms.CharField(max_length=15)
	first_name = forms.CharField(max_length=15)
	last_name = forms.CharField(max_length=15)
	email = forms.EmailField(widget=forms.EmailInput)

class CreateAccountForm(forms.Form):
	username = forms.CharField(max_length=15)
	password = forms.CharField(max_length=15)
	first_name = forms.CharField(max_length=15)
	last_name = forms.CharField(max_length=15)
	email = forms.EmailField(widget=forms.EmailInput)
   
class PasswordResetForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput)

class DocumentForm(forms.Form):
     docfile = forms.FileField(
         label='Select a file',
         help_text='max. 42 megabytes'
     )

class CreateUnitForm(forms.Form):
	unit_name = forms.CharField(max_length=50)
	unit_code = forms.CharField(max_length=50)
	captcha = CaptchaField()

class CreateSubpageForm(forms.Form):
	subpage_name = forms.CharField(max_length=50)
	captcha = CaptchaField()
 
class EditUnitForm(forms.Form):
	unit_name = forms.CharField(max_length=50)
	unit_code = forms.CharField(max_length=50)
	approval = forms.NullBooleanField()
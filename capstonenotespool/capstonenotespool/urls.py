"""capstonenotespool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from notespool import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='index'),
	url(r'^oauth/', include('social_django.urls', namespace='social')),
	url(r'^login/', views.loginuser, name='login'),
	url(r'^administrator/', views.administrator, name='administrator'),
	url(r'^edit_account/(?P<account>[^/]+)', views.editAccount, name='editAccounts'),
	url(r'^delete_account/(?P<account>[^/]+)', views.deleteAccount, name='deleteAccounts'),
	url(r'^logout/', views.logout, name='logout'),
	url(r'^account/', views.account, name='account'),
	url(r'^activation/',views.activate, name='activation'),
	url(r'^createaccount/', views.createaccount, name='createaccount'),
	url(r'^privacypolicy/', views.privacypolicy, name='privacypolicy'),
	url(r'^useragreement/', views.useragreement, name='useragreement'),
	url(r'^passwordreset/', views.passwordreset, name='passwordreset'),
	url(r'^aboutus/', views.aboutus, name='aboutus'),
	url(r'^contact/', views.contact, name='contact'),
	url(r'^notespool/', views.notespool, name='notespool'),
	

    
]

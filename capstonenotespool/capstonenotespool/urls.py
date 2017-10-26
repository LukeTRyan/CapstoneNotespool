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
from django.conf.urls.static import static
from django.conf import settings
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
	url(r'^create_account/', views.createAccount, name='createaccount'),
	url(r'^view_unit/', views.view_unit, name='viewunit'),
	url(r'^create_unit/', views.create_unit, name='createunit'),
	url(r'^delete_unit/(?P<unitid>[^/]+)', views.delete_unit, name='deleteunit'),
	url(r'^edit_unit/(?P<unitid>[^/]+)', views.edit_unit, name='editunit'),
	url(r'^approve_unit/(?P<unitid>[^/]+)', views.approve_unit, name='approveunit'),
	url(r'^approve_subpage/(?P<subpageid>[^/]+)', views.approve_subpage, name='approvesubpage'),
	url(r'^delete_subpage/(?P<subpageid>[^/]+)', views.delete_subpage, name='deletesubpage'),
	url(r'^logout/', views.logout, name='logout'),
	url(r'^account/', views.account, name='account'),
	url(r'^edit_profile/', views.edit_profile, name='edit_profile'),
	url(r'^activation/',views.activate, name='activation'),
	url(r'^activatereset/',views.activatereset, name='activatereset'),
	url(r'^registeraccount/', views.registeraccount, name='registeraccount'),
	url(r'^privacypolicy/', views.privacypolicy, name='privacypolicy'),
	url(r'^useragreement/', views.useragreement, name='useragreement'),
	url(r'^passwordreset/', views.passwordreset, name='passwordreset'),
	url(r'^aboutus/', views.aboutus, name='aboutus'),
	url(r'^contact/', views.contact, name='contact'),
	url(r'^faq/', views.faq, name='faq'),
	url(r'^notespool/', views.notespool, name='notespool'),
    url(r'^unit_page/(?P<unitname>[^/]+)', views.unit_page, name='unit_page'),
	url(r'^unit_subpage/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)', views.unit_subpage, name='unit_subpage'),
	url(r'^create_subpage/(?P<unitname>[^/]+)', views.create_subpage, name='create_subpage'),
	url(r'^view_subpages/', views.view_subpages, name='view_subpages'),
	url(r'^create_quiz/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)', views.create_quiz, name='create_quiz'),
	url(r'^delete_quiz/(?P<unitname>[^/]+)/(?P<examid>[^/]+)', views.delete_quiz, name='delete_quiz'),
	url(r'edit_question/(?P<questionid>[^/]+)/(?P<examid>[^/]+)/(?P<examslug>[^/]+)', views.edit_question, name='edit_question'),
	url(r'^edit_quiz/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)/(?P<examid>[^/]+)', views.edit_quiz, name='edit_quiz'),
	url(r'^take_quiz/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)/(?P<examid>[^/]+)', views.take_quiz, name='take_quiz'),
	url(r'^create_text_field/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)', views.create_text_field, name='create_text_field'),
	url(r'^delete_text_field/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)/(?P<notesid>[^/]+)', views.delete_text_field, name='delete_text_field'),
	url(r'^edit_text_field/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)/(?P<notesid>[^/]+)', views.edit_text_field, name='edit_text_field'),
	url(r'^upload_document/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)/(?P<notesid>[^/]+)', views.upload_document, name='upload_document'),
	url(r'^delete_document/(?P<documentpk>[^/]+)', views.delete_document, name='delete_document'),
	url(r'^add_comment/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)/(?P<notesid>[^/]+)', views.add_comment, name='add_comment'),
 	url(r'^edit_comment/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)/(?P<notesid>[^/]+)/(?P<commentid>[^/]+)', views.edit_comment, name='edit_comment'),
 	url(r'^remove_comment/(?P<unitname>[^/]+)/(?P<subpagename>[^/]+)/(?P<notesid>[^/]+)/(?P<commentid>[^/]+)', views.remove_comment, name='remove_comment'),
	url(r'^subscribed_units/', views.subscribed_units, name='subscribed_units'),
	url(r'^subscribe/(?P<unitid>[^/]+)', views.subscribe, name='subscribe'),
	url(r'^unsubscribe/(?P<unitid>[^/]+)', views.unsubscribe, name='unsubscribe'),
	url(r'^list/$', views.list, name='list'),
    url(r'^captcha/', include('captcha.urls')),
	url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

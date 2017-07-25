from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html', {})

def login(request):
    return render(request, 'login.html', {})

def account(request):
    return render(request, 'account.html', {})

def aboutus(request):
    return render(request, 'aboutus.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def notespool(request):
    return render(request, 'notespool.html', {})
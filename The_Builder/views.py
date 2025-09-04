from django.shortcuts import render

def home(request):
    return render(request, 'base.html')


def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')
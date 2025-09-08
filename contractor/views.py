from django.shortcuts import render

# Create your views here.
def contractor_home(request):
    return render(request, 'home.html')
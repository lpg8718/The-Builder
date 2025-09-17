from django.shortcuts import render

# Create your views here.
def contractor_home(request):
    return render(request, 'contractor_home.html')

def contractore_view_profile(request):
    return render(request, 'contractor_view_profile.html')
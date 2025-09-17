
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contractor_home, name='home'),
    path('profile/', views.contractore_view_profile, name='profile'),
]

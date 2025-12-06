
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.thekedar_home, name='home'),
    path('profile/', views.thekedar_profile, name='profile'),
    path('profile_edit/', views.thekedar_profile_edit, name='profile_edit'),
    path('projects_all/', views.thekedar_projects_all, name='projects_all'),
]

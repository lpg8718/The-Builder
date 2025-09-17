
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.worker_home, name='home'),
]

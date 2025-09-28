
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.contractor_home, name='home'),
    path('profile/', views.contractore_view_profile, name='profile'),
    path('profile_edit/',views.contractore_edit_profile)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

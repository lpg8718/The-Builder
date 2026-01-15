
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.contractor_home, name='home'),
    path('profile/', views.contractore_view_profile, name='profile'),
    path('profile_edit/',views.contractore_edit_profile),
    path('project_page1/',views.project_page1),
    path('project_page1/add_project/',views.add_project),
    path('project_applications/',views.project_application),
    path('project_page1/view_project/<int:project_id>/',views.view_project,name="view_project"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

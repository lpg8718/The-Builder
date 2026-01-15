
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.thekedar_home, name='home'),
    path('profile/', views.thekedar_profile, name='profile'),
    path('profile_edit/', views.thekedar_profile_edit, name='profile_edit'),
    path('projects_all/', views.thekedar_projects_all, name='projects_all'),
    path('apply_project/', views.apply_project, name='apply_project'),
    path('project_details/', views.project_details, name='project_detail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
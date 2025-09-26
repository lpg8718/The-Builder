
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('contractor/', include('contractor.urls')),
    path('thekedar/', include('thekedar.urls')),
    path('worker/', include('worker.urls')),
    path("api/", include("api.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

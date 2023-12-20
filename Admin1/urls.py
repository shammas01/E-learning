from django.urls import path
from . views import admin_login
from django.contrib.auth.models import UserManager


urlpatterns = [
    path('admin/login/',admin_login,name='admin_login')
    
]

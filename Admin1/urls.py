from django.urls import path
from . views import admin_login,admin_home,admin_logout
from django.contrib.auth.models import UserManager


urlpatterns = [
    path('login/',admin_login,name='admin_login'),
    path('home/', admin_home, name='admin_home'),
    path('logout/', admin_logout, name='admin_logout'),
    
]

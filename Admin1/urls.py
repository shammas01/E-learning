from django.urls import path
from . views import (admin_login,
                     admin_home,
                     admin_logout,
                     Admin_User_listing,
                     User_profile,
                     Admin_tutor_listing,
                     Tutor_Profile,
                     approve_tutor,
                     block_unblock_tutor,
                     tutor_couse_details)
from django.contrib.auth.models import UserManager


urlpatterns = [
    path('',admin_login,name='admin_login'),
    path('home/', admin_home, name='admin_home'),
    path('logout/', admin_logout, name='admin_logout'),

    path('tutors/',Admin_tutor_listing,name='admin_tutors'),
    path('users/',Admin_User_listing,name='admin_users'),

    path('tutor/<str:pk>/',Tutor_Profile,name='tutor_profile'),
    path('user/<str:pk>/',User_profile,name='admin_profile_page'),
    path('tutors/<int:pk>/approve/', approve_tutor, name='approve_tutor'),
    path('tutor/<int:pk>/block/', block_unblock_tutor, name='block_tutor'),
    path('course_details/<int:pk>/',tutor_couse_details,name='tutor_course'),

]

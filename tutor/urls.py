from django.urls import path
from . views import TutorRegisterView

urlpatterns = [
    path('register/',TutorRegisterView.as_view(),name='tutor_register')
]

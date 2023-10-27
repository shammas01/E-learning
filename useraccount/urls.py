from django.urls import path
from . views import EmailGetView

urlpatterns = [
    path('emailsend/',EmailGetView.as_view(),name='email_get')
]
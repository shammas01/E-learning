from django.urls import path
from .views import (
    RegisterEmailSendView,
    loginView,
    GoogleSocialAuthView,
    EmailVerify,
)

urlpatterns = [
    path("emailsend/", RegisterEmailSendView.as_view(), name="email_get"),
    path('emailverify/',EmailVerify.as_view()),
    path("login/", loginView.as_view(), name="otp_verifiy"),
    path("googleaut/", GoogleSocialAuthView.as_view(), name="googelauth"),
]

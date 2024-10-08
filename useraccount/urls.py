from django.urls import path
from .views import (
    RegisterEmailSendView,
    loginView,
    GoogleSocialAuthView,
    EmailVerify,
    Register #for sample
)

urlpatterns = [
    path("register/", RegisterEmailSendView.as_view(), name="email_get"),
    path('emailverify/',EmailVerify.as_view()),
    path("login/", loginView.as_view(), name="otp_verifiy"),
    path("googleaut/", GoogleSocialAuthView.as_view(), name="googelauth"),

    path('samplereg/', Register.as_view(), name="samplereg")
]

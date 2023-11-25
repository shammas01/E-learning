from django.urls import path
from .views import (
    EmailOtpSendView,
    EmailOtpVerifyView,
    GoogleSocialAuthView,
    
    
)

urlpatterns = [
    path("emailsend/", EmailOtpSendView.as_view(), name="email_get"),
    path("emailotpverify/", EmailOtpVerifyView.as_view(), name="otp_verifiy"),
    path("googleaut/", GoogleSocialAuthView.as_view(), name="googelauth"),
]

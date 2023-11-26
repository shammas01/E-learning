from django.urls import path
from .views import (
    RegisterEmailSendView,
    loginView,
    GoogleSocialAuthView,
    
    
)

urlpatterns = [
    path("emailsend/", RegisterEmailSendView.as_view(), name="email_get"),
    path("emailotpverify/", loginView.as_view(), name="otp_verifiy"),
    path("googleaut/", GoogleSocialAuthView.as_view(), name="googelauth"),
]

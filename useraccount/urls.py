from django.urls import path
from .views import (
    EmailOtpSendView,
    EmailOtpVerifyView,
    GoogleSocialAuthView,
    VerifyMobileNumber,
    PhoneOtpVerificationView,
    EmailUpdatdOtpView,
)

urlpatterns = [
    path("emailsend/", EmailOtpSendView.as_view(), name="email_get"),
    path("emailotpverify/", EmailOtpVerifyView.as_view(), name="otp_verifiy"),
    path("googleaut/", GoogleSocialAuthView.as_view(), name="googelauth"),
    path("phoneverify/", VerifyMobileNumber.as_view(), name="verifiy_phone_number"),
    path("phoneotpverify/", PhoneOtpVerificationView.as_view(), name=" phoneotp"),
    path("emailupdate/", EmailUpdatdOtpView.as_view(), name="email_update_otp"),
]

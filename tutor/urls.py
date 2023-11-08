from django.urls import path
from .views import TutorRrgistrationView, PhoneOtpVerifyView

urlpatterns = [
    path("register/", TutorRrgistrationView.as_view(), name="tutor_register"),
    path("otpverify/", PhoneOtpVerifyView.as_view(), name="otp_varification"),
]

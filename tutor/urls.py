from django.urls import path
from . views import TutorRrgistrationView,TutorPhoneVerification,PhoneOtpVerifyView

urlpatterns = [
    path('register/',TutorRrgistrationView.as_view(),name='tutor_register'),
    path('phoneverify/',TutorPhoneVerification.as_view(),name='phone_verify'),
    path('otpverify/',PhoneOtpVerifyView.as_view(),name='otp_varification')
]

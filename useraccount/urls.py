from django.urls import path
from . views import EmailOtpSendView,EmailOtpVerifyView,UserProfileView,GoogleSocialAuthView

urlpatterns = [
    path('emailsend/',EmailOtpSendView.as_view(),name='email_get'),
    path('otpverification/',EmailOtpVerifyView.as_view(),name='otp_verifiy'),
    path('userprofile/',UserProfileView.as_view(),name='user_profile'),
    path('googleaut/',GoogleSocialAuthView.as_view(),name='googelauth')

]
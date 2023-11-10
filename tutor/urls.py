from django.urls import path
from .views import TutorListCreateView, PhoneOtpVerifyView,TutorUpdateView

urlpatterns = [
    path("register/", TutorListCreateView.as_view(), name="tutor_register"),
    path('update/',TutorUpdateView.as_view(),name='tutor update'),
    path("otpverify/", PhoneOtpVerifyView.as_view(), name="otp_varification"),
]

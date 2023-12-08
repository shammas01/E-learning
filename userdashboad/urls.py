from django.urls import path
from . views import (CourseSearching,
                    UserProfileView,
                    LiveListing,
                    CourseListing,
                    TutorListing,
                    TutorSelect,
                    CourseSelect,
                    LiveSelect,
                    EmailUpdatdOtpView,
                    VerifyMobileNumber,
                    PhoneOtpVerificationView,
                    ShowCartView,
                    AddToCart,
                    Adtocart,  #adtocart for sample
                    Checkout,
                    PaymentAPI,
                    LiveEnrollment) 

urlpatterns = [
    path('searching/',CourseSearching.as_view(),name="course_searching"),
    path('lives/',LiveListing.as_view(),name='all_lives'),
    path('courses/',CourseListing.as_view(),name='all_course'),
    path('tutors/',TutorListing.as_view(),name='all_tutors'),

    path('tutorselect/<int:pk>/',TutorSelect.as_view(),name='one_tutor'),
    path('courseslect/<int:pk>/',CourseSelect.as_view(),name='one_course'),
    path('liveselect/<int:pk>/',LiveSelect.as_view(), name='one_live'),
   
    path("userprofile/", UserProfileView.as_view(), name="user_profile"),
    path("emailupdate/", EmailUpdatdOtpView.as_view(), name="email_update_otp"),
    path("phoneverify/", VerifyMobileNumber.as_view(), name="verifiy_phone_number"),
    path("phoneotpverify/", PhoneOtpVerificationView.as_view(), name=" phoneotp"),

    path('showcart/',ShowCartView.as_view(),name="show_cart"),
    path('addtocart/',AddToCart.as_view(),name='add_to_cart'),
    path('addtocart2/<int:pk>/',Adtocart.as_view()),

    path('checkout/',Checkout.as_view(),name='checkout'),
    path('make_payment/', PaymentAPI.as_view(), name='make_payment'),

    path('liveenroll/<int:pk>/',LiveEnrollment.as_view(),name="live_enrollment")
]

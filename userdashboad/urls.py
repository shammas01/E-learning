from django.urls import path
from . views import CourseSearching,UserProfileView,LiveListing,CourseListing,TutorListing

urlpatterns = [
    path('searching/',CourseSearching.as_view(),name="course_searching"),
    path('lives/',LiveListing.as_view(),name='all_lives'),
    path('courses/',CourseListing.as_view(),name='all_course'),
    path('tutors/',TutorListing.as_view(),name='all_tutors'),
   
    path("userprofile/", UserProfileView.as_view(), name="user_profile"),
]

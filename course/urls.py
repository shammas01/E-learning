from django.urls import path
from . views import ListCreateCourseView,RetriveUpdateDistroyView





urlpatterns = [
    path('course-details/',ListCreateCourseView.as_view(),name='course_details'),
    path('course-update/<int:pk>/',RetriveUpdateDistroyView.as_view(),name='course_update')

]


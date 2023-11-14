from django.urls import path
from . views import ListCreateCourseDetailsView,RetriveUpdateCourseDetailsView,ListCreateCourseContentView





urlpatterns = [
    path('course-details/',ListCreateCourseDetailsView.as_view(),name='course_details'),
    path('course-details/<int:pk>/',RetriveUpdateCourseDetailsView.as_view(),name='course_update'),

    path('course-content/<int:course_id>/',ListCreateCourseContentView.as_view(),name='course_content')

]


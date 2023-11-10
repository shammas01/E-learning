from django.urls import path
from . views import CreateCourseView
urlpatterns = [
    path('coursedetails/',CreateCourseView.as_view(),name='course_details')
]

from django.urls import path
from . views import CourseSearching

urlpatterns = [
    path('details/',CourseSearching.as_view(),name="course_searching")
]

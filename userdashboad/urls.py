from django.urls import path
from . views import CourseSearching,TutorSlection

urlpatterns = [
    path('details/',CourseSearching.as_view(),name="course_searching"),
    path('tutors/',TutorSlection.as_view(),name='tutor_selection')
]

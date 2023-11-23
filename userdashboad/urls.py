from django.urls import path
from . views import CourseSearching,Slide_Bar_Slection

urlpatterns = [
    path('details/',CourseSearching.as_view(),name="course_searching"),
    path('slide_bar/',Slide_Bar_Slection.as_view(),name='tutor_selection')
]

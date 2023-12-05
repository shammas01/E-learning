from django.urls import path
from . views import ListCreateCourseDetailsView,RetriveUpdateCourseDetailsView,ListCreateCourseLessontView,LessonUpdateView





urlpatterns = [
    path('course-create/',ListCreateCourseDetailsView.as_view(),name='course_details'),
    path('course-update/<int:pk>/',RetriveUpdateCourseDetailsView.as_view(),name='course_update'),

    path('list-lesson/<int:course_id>/',ListCreateCourseLessontView.as_view(),name='course_list'),
    path('update-lesson/<int:pk>/',LessonUpdateView.as_view(),name='lesson_update')

]


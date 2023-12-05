from django.urls import path
from . views import LiveDetailListCreateView,LiveDetailUpdateView,testView,send_mail_to_all_users,sendmailattime

urlpatterns = [
    path('live-create/', LiveDetailListCreateView.as_view(),name='live_create'),
    path('live-update/<int:pk>/',LiveDetailUpdateView.as_view(),name='live_update'),


    # celery...
    path('celery/',testView,name="testView"),
    path('mail/',send_mail_to_all_users,name="testmail"),
    path('scheduletime/',sendmailattime,name='mailscheduling')

]

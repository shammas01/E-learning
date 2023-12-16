from . views import index,room
from django.urls import path


urlpatterns = [
    path('index/',index, name='index'),
    path('index/<str:room_name>/', room, name='room')
]

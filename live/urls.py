from django.urls import path
from . views import LiveDetailListCreateView

urlpatterns = [
    path('live-create/', LiveDetailListCreateView.as_view(),name='live_create'),
    
]

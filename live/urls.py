from django.urls import path
from . views import LiveDetailListCreateView,LiveDetailUpdateView

urlpatterns = [
    path('live-create/', LiveDetailListCreateView.as_view(),name='live_create'),
    path('live-update/<int:pk>/',LiveDetailUpdateView.as_view(),name='live_update')

]

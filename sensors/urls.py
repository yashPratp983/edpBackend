# sensors/urls.py

from django.urls import path
from .views import TemperatureAPIView, HeartRateAPIView

urlpatterns = [
    path('temperature', TemperatureAPIView.as_view(), name='temperature-api'),
    path('heart-rate', HeartRateAPIView.as_view(), name='heart-rate-api'),
]
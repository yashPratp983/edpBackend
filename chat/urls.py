from django.urls import path,include
from .views import ChatView

urlpatterns = [
    path('chat', ChatView.as_view()),
]

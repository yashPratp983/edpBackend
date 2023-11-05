from django.urls import path,include
from .views import RegisterView, LoginView, LogoutView, UserView, VerifyPhoneNumber, ResendOTP
urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('verify', VerifyPhoneNumber.as_view()),
    path('resend', ResendOTP.as_view()),
]
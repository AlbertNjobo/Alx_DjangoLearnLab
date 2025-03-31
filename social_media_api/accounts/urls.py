# accounts/urls.py
from django.urls import path
from .views import RegisterView, ProfileView
from rest_framework.authtoken.views import obtain_auth_token # Import the built-in view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'), # Use the built-in view for login
    path('profile/', ProfileView.as_view(), name='profile'),
]
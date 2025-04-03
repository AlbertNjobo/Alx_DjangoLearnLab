# accounts/urls.py
from django.urls import path
from .views import RegisterView, ProfileView, CustomLoginView, FollowView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Use the custom login view
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', FollowView.as_view(), name='unfollow_user'),
]
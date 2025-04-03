# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView # Ensure .views can be imported

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
# Register CommentViewSet for direct access to /api/comments/{pk}/ if needed
# router.register(r'comments', CommentViewSet, basename='comment') # Uncomment if needed

# --- THIS IS THE CRUCIAL PART ---
urlpatterns = [
    # Include the URLs generated by the router
    path('', include(router.urls)),

    # Provide direct access to comment detail/update/delete via /api/comments/{pk}/
    # This uses the CommentViewSet's standard retrieve/update/destroy methods
    path('comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='comment-detail'),

    # Add a route for the feed endpoint
    path('feed/', FeedView.as_view(), name='feed'),

    # Add routes for liking and unliking posts
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]

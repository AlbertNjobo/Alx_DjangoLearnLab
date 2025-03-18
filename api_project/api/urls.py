from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Existing ListAPIView
    path('auth/token/', obtain_auth_token, name='api-token-auth'),  # Token retrieval endpoint
    path('', include(router.urls)),  # Include routes for BookViewSet
]

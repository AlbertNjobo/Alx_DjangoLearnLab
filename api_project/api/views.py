from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class BookList(generics.ListAPIView):  # ✅ This meets the task requirement
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

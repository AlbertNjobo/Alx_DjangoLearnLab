from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):  # ✅ This meets the task requirement
    queryset = Book.objects.all()
    serializer_class = BookSerializer

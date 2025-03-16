from rest_framework import serializers
from .models import Book, Author
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

        def validate(self, data):
            """
            Check that the start is before the stop.
            """
            if data['publication_date'] > datetime.date.today():
                raise serializers.ValidationError("The publication date must be in the past.")
               
            return data

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    related_books = BookSerializer(many=True, read_only=True)
     
    class Meta:
        model = Author 
        fields = [id, 'name', 'related_books']
# 
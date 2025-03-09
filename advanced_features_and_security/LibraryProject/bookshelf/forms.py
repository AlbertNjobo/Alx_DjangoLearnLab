from django import forms
from .models import Article
from .models import Book

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date']
    
    def clean_isbn(self):
        """Security: Validate ISBN format"""
        isbn = self.cleaned_data['isbn']
        if not isbn.isdigit() or len(isbn) != 13:
            raise forms.ValidationError("ISBN must be a 13-digit number")
        return isbn

# Import the Book model
from bookshelf.models import Book

# CREATE
book = Book.objects.create(
    title="1984", 
    author="George Orwell", 
    publication_year=1949
)
print(f"Created book: {book}")

# Import the Book model
from bookshelf.models import Book

# RETRIEVE
retrieved_book = Book.objects.get(title="1984")
print(f"Retrieved Book ID: {retrieved_book.id}")
print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Publication Year: {retrieved_book.publication_year}")

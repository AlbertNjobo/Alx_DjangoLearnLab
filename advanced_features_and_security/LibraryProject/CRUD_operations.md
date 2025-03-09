# Import the Book model
from bookshelf.models import Book

# CREATE
book = Book.objects.create(
    title="1984", 
    author="George Orwell", 
    publication_year=1949
)
print(f"Created book: {book}")

# RETRIEVE
retrieved_book = Book.objects.get(title="1984")
print(f"Retrieved Book ID: {retrieved_book.id}")
print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Publication Year: {retrieved_book.publication_year}")

# UPDATE
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated book title: {book.title}")

# DELETE
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted")

# Verify deletion
try:
    Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Book successfully deleted")

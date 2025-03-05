# Import the Book model
from bookshelf.models import Book

# DELETE
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted")

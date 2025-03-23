from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from api.models import Author, Book
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Create an author instance for test purposes
        self.author = Author.objects.create(name="George Orwell")

    def test_create_book(self):
        """Test creating a book"""
        url = reverse('book-create')  # Make sure your URL pattern for create is named 'book-create'
        data = {
            'title': 'Animal Farm',
            'publication_date': '1945-08-17',  # Correct the field to publication_date
            'author': self.author.id
        }
        response = self.client.post(url, data, format='json')

        # Assert that the book was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'Animal Farm')

    def test_get_books(self):
        """Test retrieving all books"""
        url = reverse('book-list')  # URL to retrieve book list
        response = self.client.get(url)

        # Assert that we can retrieve the books
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No books initially, adjust as needed after test creation

    def test_get_book(self):
        """Test retrieving a single book"""
        # Create a book instance
        book = Book.objects.create(
            title="1984", 
            publication_date='1949-06-08', 
            author=self.author
        )
        url = reverse('book-detail', args=[book.id])  # Get details of a single book
        response = self.client.get(url)

        # Assert that we can retrieve the correct book
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')

    def test_update_book(self):
        """Test updating a book"""
        book = Book.objects.create(
            title="1984", 
            publication_date='1949-06-08', 
            author=self.author
        )
        url = reverse('book-update', args=[book.id])  # URL for book update
        data = {
            'title': '1984 - Updated',  # Update the title
            'publication_date': '1949-06-09',  # Update the publication date
            'author': self.author.id
        }
        response = self.client.put(url, data, format='json')

        # Assert that the book was updated
        book.refresh_from_db()  # Refresh the object to get the updated values from the database
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book.title, '1984 - Updated')
        self.assertEqual(book.publication_date.strftime('%Y-%m-%d'), '1949-06-09')

    def test_delete_book(self):
        """Test deleting a book"""
        book = Book.objects.create(
            title="1984", 
            publication_date='1949-06-08', 
            author=self.author
        )
        url = reverse('book-delete', args=[book.id])  # URL for book delete
        response = self.client.delete(url)

        # Assert that the book is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from api.models import Book
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Create test books
        self.book1 = Book.objects.create(title="Book One", author="Author One", publication_date="2020-01-01")
        self.book2 = Book.objects.create(title="Book Two", author="Author Two", publication_date="2021-01-01")

    def test_create_book(self):
        """Test creating a book"""
        url = reverse('book_all-list')  # DefaultRouter generates this name
        data = {
            "title": "New Book",
            "author": "New Author",
            "publication_date": "2022-01-01"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_get_books(self):
        """Test retrieving all books"""
        url = reverse('book_all-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_book(self):
        """Test retrieving a single book"""
        url = reverse('book_all-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Book One")

    def test_update_book(self):
        """Test updating a book"""
        url = reverse('book_all-detail', args=[self.book1.id])
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "publication_date": "2023-01-01"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")
        self.assertEqual(self.book1.author, "Updated Author")

    def test_delete_book(self):
        """Test deleting a book"""
        url = reverse('book_all-detail', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        url = f"{reverse('book_all-list')}?author=Author One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], "Author One")

    def test_order_books_by_publication_date(self):
        """Test ordering books by publication date"""
        url = f"{reverse('book_all-list')}?ordering=publication_date"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dates = [book['publication_date'] for book in response.data]
        self.assertEqual(dates, sorted(dates))

    def test_permissions(self):
        """Test that unauthenticated users cannot access the API"""
        self.client.credentials()  # Remove authentication
        url = reverse('book_all-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

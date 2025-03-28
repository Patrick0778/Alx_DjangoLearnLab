from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Author

class BookAPITestCase(TestCase):
    def setUp(self):
        """Set up test environment with a user, an author, and a book."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )

        self.book_url = f"/books/{self.book.id}/"
        self.book_create_url = "/books/create/"
        self.book_update_url = f"/books/update/{self.book.id}/"
        self.book_delete_url = f"/books/delete/{self.book.id}/"

    def test_list_books(self):
        """Test retrieving all books."""
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_book_detail(self):
        """Test retrieving a single book."""
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_create_book_authenticated(self):
        """Test creating a book when authenticated."""
        self.client.login(username='testuser', password='testpass')  # Authenticate user
        data = {"title": "New Book", "publication_year": 2024, "author": self.author.id}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should fail)."""
        data = {"title": "New Book", "publication_year": 2024, "author": self.author.id}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Test updating a book when authenticated."""
        self.client.login(username='testuser', password='testpass')  # Authenticate user
        data = {"title": "Updated Book Title", "publication_year": 2025, "author": self.author.id}
        response = self.client.put(self.book_update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book Title")

    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication (should fail)."""
        data = {"title": "Updated Book Title", "publication_year": 2025, "author": self.author.id}
        response = self.client.put(self.book_update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        """Test deleting a book when authenticated."""
        self.client.login(username='testuser', password='testpass')  # Authenticate user
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication (should fail)."""
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_books_authenticated(self):
        """Test filtering books by title when authenticated."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get("/books/?title=Test Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Test Book")

    def test_search_books_authenticated(self):
        """Test searching for books by title when authenticated."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get("/books/?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_books_authenticated(self):
        """Test ordering books by publication_year when authenticated."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get("/books/?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

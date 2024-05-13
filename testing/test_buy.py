from django.test import TestCase, client as django_client
from django.contrib.auth.models import User
from library_app.models import Book, Client
from rest_framework import status

book_attrs = {'title': 'ABC', 'volume': 1, 'price': 1}

class TestPurchase(TestCase):
    _page_url = '/buy/'

    def setUp(self):
        self.user = User.objects.create(username='user', password='user')
        self.client = Client.objects.create(user=self.user, money=0)
        self.api_client = django_client.Client()
        self.api_client.force_login(self.user)
    
    def test_insufficient_funds(self):
        book = Book.objects.create(**book_attrs)
        self.api_client.post(f'{self._page_url}?id={book.id}', {})
        self.client.refresh_from_db()

        self.assertEqual(self.client.money, 0)
        self.assertNotIn(book, self.client.books.all())

    def test_successful(self):
        book = Book.objects.create(**book_attrs)
        self.client.money = book.price
        self.client.save()

        self.api_client.post(f'{self._page_url}?id={book.id}', {})
        self.client.refresh_from_db()

        self.assertEqual(self.client.money, 0)
        self.assertIn(book, self.client.books.all())

    def test_repeated_purchase(self):
        book = Book.objects.create(**book_attrs)
        self.client.money = book.price
        self.client.save()

        self.api_client.post(f'{self._page_url}?id={book.id}', {})
        self.client.refresh_from_db()

        self.assertEqual(self.client.money, 0)
        self.assertIn(book, self.client.books.all())

        self.api_client.post(f'{self._page_url}?id={book.id}', {})
        self.client.refresh_from_db()

        self.assertEqual(self.client.money, 0)
        self.assertEqual(len(self.client.books.filter(id=book.id)), 1)

    def test_redirect_no_id(self):
        response = self.api_client.post(f'{self._page_url}', {})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_redirect_invalid_id(self):
        book = Book.objects.create(**book_attrs)

        response = self.api_client.post(f'{self._page_url}?id={book.id}123', {})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

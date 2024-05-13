from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime, timezone
from django.contrib.auth.models import User

from library_app import models

def create_test(attr, value):
    def new_test(self):
        data = self._creation_attrs.copy()
        data[attr] = value
        with self.assertRaises(ValidationError):
            self._model_class.objects.create(**data)
    return new_test

def create_test_save(attr, value):
    def new_test(self):
        data = self._creation_attrs.copy()
        instance = self._model_class.objects.create(**data)
        setattr(instance, attr, value)
        with self.assertRaises(ValidationError):
            instance.save()
    return new_test

def create_model_test(model_class, creation_attrs, tests):
    class ModelTest(TestCase):
        _model_class = model_class
        _creation_attrs = creation_attrs

        def test_successful_creation(self):
            self._model_class.objects.create(**self._creation_attrs)

    for num, values in enumerate(tests):
        attr, value = values
        setattr(ModelTest, f'test_create_{attr}_{num}', create_test(attr, value))
        setattr(ModelTest, f'test_save_{attr}_{num}', create_test_save(attr, value))

    return ModelTest

book_attrs = {'title': 'ABC', 'type': 'book', 'volume': 1}
genre_attrs = {'name': 'ABC'}
author_attrs = {'full_name': 'ABC'}

book_tests = (
    ('volume', -1),
    ('year', 3000),
    ('price', -10),
    ('type', 'Vadim'),
)

BookModelTest = create_model_test(models.Book, book_attrs, book_tests)
AuthorModelTest = create_model_test(models.Author, author_attrs, [])
GenreModelTest = create_model_test(models.Genre, genre_attrs, [])

PAST_YEAR = 2007
FUTURE_YEAR = 3000

valid_tests = (
    (models.check_created, datetime(PAST_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_modified, datetime(PAST_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_positive, 1),
    (models.check_year, PAST_YEAR),
)
invalid_tests = (
    (models.check_created, datetime(FUTURE_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_modified, datetime(FUTURE_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_positive, -1),
    (models.check_year, FUTURE_YEAR),
)

def create_validation_test(validator, value, valid=True):
    if valid:
        return lambda _: validator(value)
    def test(self):
        with self.assertRaises(ValidationError):
            validator(value)
    return test

valid_methods = {
    f'test_valid_{args[0].__name__}': create_validation_test(*args) for args in valid_tests
}
invalid_methods = {
    f'test_invalid_{args[0].__name__}': create_validation_test(*args, valid=False) for args in invalid_tests
}

TestValidators = type('TestValidators', (TestCase,), valid_methods | invalid_methods)

test_str_data = (
    (models.Book, book_attrs, '"ABC", book, 1 pages'),
    (models.Genre, genre_attrs, 'ABC'),
    (models.Author, author_attrs, 'ABC'),
)

def create_str_test(model, attrs, expected):
    def test(self):
        self.assertEqual(str(model.objects.create(**attrs)), expected)
    return test

test_str_methods = {f'test_{args[0].__name__}': create_str_test(*args) for args in test_str_data}
TestStr = type('TestStr', (TestCase,), test_str_methods)

class TestLinks(TestCase):
    def test_book_genre(self):
        genre = models.Genre.objects.create(**genre_attrs)
        book = models.Book.objects.create(**book_attrs)
        book.genres.add(genre)

        link = models.BookGenre.objects.get(book=book, genre=genre)

        self.assertEqual(str(link), f'{book} - {genre}')

    def test_book_author(self):
        author = models.Author.objects.create(**author_attrs)
        book = models.Book.objects.create(**book_attrs)
        book.authors.add(author)

        link = models.BookAuthor.objects.get(book=book, author=author)

        self.assertEqual(str(link), f'{book} - {author}')

    def test_book_client(self):
        user = User.objects.create(username='user', password='user')
        client = models.Client.objects.create(user=user)
        book = models.Book.objects.create(**book_attrs)
        client.books.add(book)

        link = models.BookClient.objects.get(book=book, client=client)

        self.assertEqual(str(link), f'{book} - {client}')

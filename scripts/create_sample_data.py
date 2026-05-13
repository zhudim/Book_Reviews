import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookreview.settings')
os.environ.setdefault('USE_SQLITE', 'True')

django.setup()

from django.contrib.auth import get_user_model
from books.models import Book, Genre
from reviews.models import ReadingList, Review

User = get_user_model()

if __name__ == '__main__':
    if User.objects.filter(username='reader1').exists():
        print('Sample data already exists.')
        exit(0)

    genres = [
        ('Fantasy', 'fantasy'),
        ('Science Fiction', 'sci-fi'),
        ('Non-fiction', 'non-fiction'),
    ]
    genre_objs = []
    for name, slug in genres:
        genre_objs.append(Genre.objects.get_or_create(name=name, slug=slug)[0])

    books = [
        {'title': 'The Light Between Worlds', 'author': 'Kayla Ancrum', 'description': 'A magical modern fantasy about belonging, stories and family.', 'published_date': '2022-05-03', 'genres': ['fantasy']},
        {'title': 'Deep Learning with Python', 'author': 'Francois Chollet', 'description': 'A practical guide to deep learning using the Keras library.', 'published_date': '2017-10-28', 'genres': ['non-fiction']},
        {'title': 'The Martian', 'author': 'Andy Weir', 'description': 'A gripping survival story of an astronaut stranded on Mars.', 'published_date': '2014-02-11', 'genres': ['sci-fi']},
    ]

    book_objs = []
    for item in books:
        book = Book.objects.create(
            title=item['title'],
            author=item['author'],
            description=item['description'],
            published_date=item['published_date'],
        )
        for slug in item['genres']:
            book.genres.add(Genre.objects.get(slug=slug))
        book_objs.append(book)

    user1 = User.objects.create_user(username='reader1', email='reader1@example.com', password='password123')
    user2 = User.objects.create_user(username='critic', email='critic@example.com', password='password123')

    Review.objects.create(user=user1, book=book_objs[0], title='Чарівна історія', body='Ця книга змушує мріяти й вірити в магію.', rating=5)
    Review.objects.create(user=user2, book=book_objs[2], title='Неймовірний трилер', body='Швидко, цікаво і дуже напружено.', rating=4)

    ReadingList.objects.create(user=user1, book=book_objs[1], status=ReadingList.STATUS_WANT)
    ReadingList.objects.create(user=user1, book=book_objs[0], status=ReadingList.STATUS_READ)

    print('Sample data created.')

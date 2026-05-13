from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    published_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse('books:detail', args=[self.id])

    @property
    def average_rating(self):
        approved_reviews = self.reviews.filter(is_approved=True)
        if not approved_reviews.exists():
            return 0
        return round(approved_reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0, 1)

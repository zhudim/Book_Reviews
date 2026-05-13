from django.conf import settings
from django.db import models


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['user', 'book']]

    def __str__(self):
        return f"{self.title} ({self.rating}/10)"


class ReadingList(models.Model):
    STATUS_WANT = 'want'
    STATUS_READ = 'read'
    STATUS_CHOICES = [
        (STATUS_WANT, 'Want to Read'),
        (STATUS_READ, 'Read'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reading_list')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='list_entries')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_WANT)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']
        unique_together = [['user', 'book']]

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"

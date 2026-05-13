from django.urls import path

from .views import (
    AddReviewView,
    ReadingListView,
    ReviewDeleteView,
    ReviewUpdateView,
    toggle_reading_status,
)

app_name = 'reviews'

urlpatterns = [
    path('book/<int:book_id>/add/', AddReviewView.as_view(), name='add_review'),
    path('edit/<int:pk>/', ReviewUpdateView.as_view(), name='edit_review'),
    path('delete/<int:pk>/', ReviewDeleteView.as_view(), name='delete_review'),
    path('library/', ReadingListView.as_view(), name='library'),
    path('book/<int:book_id>/toggle/', toggle_reading_status, name='toggle_reading_status'),
]

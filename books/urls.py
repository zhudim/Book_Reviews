from django.urls import path

from .views import BookCreateView, BookDeleteView, BookDetailView, BookListView, BookUpdateView

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('book/add/', BookCreateView.as_view(), name='create'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='delete'),
]

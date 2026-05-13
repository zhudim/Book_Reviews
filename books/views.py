from django.db.models import Avg, Q
from django.views.generic import DetailView, ListView

from .models import Book, Genre
from reviews.models import ReadingList


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.prefetch_related('genres').all()
        query = self.request.GET.get('q', '').strip()
        genre = self.request.GET.get('genre', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query)
            )
        if genre:
            queryset = queryset.filter(genres__slug=genre)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['search_term'] = self.request.GET.get('q', '')
        context['selected_genre'] = self.request.GET.get('genre', '')
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.filter(is_approved=True).select_related('user')
        context['average_rating'] = self.object.average_rating
        if self.request.user.is_authenticated:
            entry = ReadingList.objects.filter(user=self.request.user, book=self.object).first()
            context['reading_status'] = entry.status if entry else None
        return context

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count, Q
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy

from .forms import BookForm
from .models import Book, Genre
from reviews.models import ReadingList

GENRE_TRANSLATIONS = {
    'fantasy': 'Фентезі',
    'non-fiction': 'Нон-фікшн',
    'sci-fi': 'Наукова фантастика',
    'science-fiction': 'Наукова фантастика',
    'mystery': 'Детектив',
    'romance': 'Роман',
    'history': 'Історія',
    'biography': 'Біографія',
    'self-help': 'Саморозвиток',
    'young-adult': 'Молодіжна література',
    'poetry': 'Поезія',
}


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.prefetch_related('genres').all()
        query = self.request.GET.get('q', '').strip()
        genre = self.request.GET.get('genre', '').strip()
        sort = self.request.GET.get('sort', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(author__icontains=query)
                | Q(description__icontains=query)
                | Q(reviews__title__icontains=query)
                | Q(reviews__body__icontains=query)
                | Q(reviews__user__username__icontains=query)
            )
        if genre:
            queryset = queryset.filter(genres__slug=genre)

        queryset = queryset.annotate(
            avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True)),
            reviews_count=Count('reviews', filter=Q(reviews__is_approved=True)),
        )

        if sort == 'rating':
            queryset = queryset.order_by('-avg_rating', '-created_at', 'title')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('title')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = list(Genre.objects.all())
        for genre in genres:
            genre.display_name = GENRE_TRANSLATIONS.get(genre.slug, genre.name)
        context['genres'] = genres
        context['search_term'] = self.request.GET.get('q', '')
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['sort'] = self.request.GET.get('sort', '')
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return (
            Book.objects.prefetch_related('genres')
            .annotate(
                avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True)),
                reviews_count=Count('reviews', filter=Q(reviews__is_approved=True)),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.filter(is_approved=True).select_related('user')
        context['average_rating'] = self.object.avg_rating or 0
        context['genres'] = [GENRE_TRANSLATIONS.get(genre.slug, genre.name) for genre in self.object.genres.all()]
        if self.request.user.is_authenticated:
            entry = ReadingList.objects.filter(user=self.request.user, book=self.object).first()
            context['reading_status'] = entry.status if entry else None
        return context


class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_message = 'Книга успішно додана!'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати нову книгу'
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_message = 'Книга успішно оновлена!'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редагувати "{self.object.title}"'
        return context


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:list')
    success_message = 'Книга успішно видалена!'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

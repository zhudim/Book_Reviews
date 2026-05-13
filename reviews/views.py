from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from books.models import Book
from .forms import ReviewForm
from .models import ReadingList, Review


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        if Review.objects.filter(user=request.user, book=self.book).exists():
            return redirect(self.book.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = self.book
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context

    def get_success_url(self):
        return self.book.get_absolute_url()


class ReviewOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user


class ReviewUpdateView(LoginRequiredMixin, ReviewOwnerMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_success_url(self):
        return self.object.book.get_absolute_url()


class ReviewDeleteView(LoginRequiredMixin, ReviewOwnerMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('books:list')


class ReadingListView(LoginRequiredMixin, ListView):
    model = ReadingList
    template_name = 'reviews/reading_list.html'
    context_object_name = 'entries'
    paginate_by = 12

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user).select_related('book')


@login_required
@require_POST
def toggle_reading_status(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    status = request.POST.get('status', ReadingList.STATUS_WANT)
    if status not in dict(ReadingList.STATUS_CHOICES):
        status = ReadingList.STATUS_WANT

    entry, created = ReadingList.objects.get_or_create(user=request.user, book=book)
    entry.status = status
    entry.save()
    return redirect(book.get_absolute_url())

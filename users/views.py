from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from reviews.models import ReadingList
from .forms import ProfileForm, UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Реєстрація успішна. Увійдіть, будь ласка.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile
    review_count = request.user.reviews.count()
    reading_count = request.user.reading_list.count()
    want_count = request.user.reading_list.filter(status=ReadingList.STATUS_WANT).count()
    read_count = request.user.reading_list.filter(status=ReadingList.STATUS_READ).count()
    recent_reviews = request.user.reviews.select_related('book')[:3]
    
    return render(
        request,
        'users/profile.html',
        {
            'profile': profile,
            'review_count': review_count,
            'reading_count': reading_count,
            'want_count': want_count,
            'read_count': read_count,
            'recent_reviews': recent_reviews,
        },
    )


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль оновлено.')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return render(request, 'registration/logged_out.html')

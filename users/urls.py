from django.urls import path

from .views import edit_profile, profile, register

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]

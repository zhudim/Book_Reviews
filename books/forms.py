from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'cover', 'ebook', 'genres', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва книги',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опис книги',
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'ebook': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.epub,.mobi',
            }),
            'genres': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input',
            }),
            'published_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'title': 'Назва книги',
            'author': 'Автор',
            'description': 'Опис',
            'cover': 'Обкладинка',
            'ebook': 'Електронна книга',
            'genres': 'Жанри',
            'published_date': 'Дата видання',
        }

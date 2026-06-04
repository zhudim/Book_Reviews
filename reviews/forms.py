from django import forms
from django.utils.safestring import mark_safe

from .models import Review


class StarRatingWidget(forms.widgets.Widget):
    """Custom widget for 1-10 star rating input"""
    
    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render 10 clickable stars for rating"""
        if attrs is None:
            attrs = {}
        
        html_parts = ['<div class="star-rating-widget">']
        
        for i in range(1, 11):
            checked = 'checked' if str(value) == str(i) else ''
            html_parts.append(
                f'<label for="{name}_{i}" class="star-rating-label" data-value="{i}">'
                f'  <input type="radio" name="{name}" value="{i}" {checked} '
                f'         id="{name}_{i}" class="star-rating-input d-none">'
                f'  <span class="star-icon">★</span>'
                f'</label>'
            )
        
        html_parts.append('</div>')
        return mark_safe(''.join(html_parts))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'body', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Назва рецензії (обов\'язково)',
            }),
            'rating': StarRatingWidget(attrs={'class': 'star-rating-input'}),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Ваша рецензія (максимум 2000 символів)...',
                'maxlength': '2000',
            }),
        }
        labels = {
            'title': 'Заголовок',
            'rating': 'Оцінка',
            'body': 'Текст рецензії',
        }

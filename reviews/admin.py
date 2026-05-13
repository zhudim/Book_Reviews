from django.contrib import admin
from .models import ReadingList, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved')
    search_fields = ('title', 'body', 'user__username', 'book__title')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Approve selected reviews'


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'added_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')

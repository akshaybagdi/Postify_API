from django.contrib import admin
from .models.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'updated_at')
    search_fields = ('content', 'user__username', 'post__title')
    list_filter = ('created_at',)

from django.contrib import admin
from .models.models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at', 'is_published',
                    'rating', 'tags_list')  # Fields to display in the list view
    list_filter = ('category', 'is_published', 'author')  # Filters in the admin panel
    search_fields = ('title', 'content')  # Searchable fields in the admin panel
    ordering = ('-created_at',)  # Default ordering of posts (by creation date, descending)
    list_per_page = 10  # Number of posts per page in the admin list view

    # You can add more configurations as needed
    def tags_list(self, obj):
        # Custom method to display the tags as a comma-separated list
        return ", ".join(tag.name for tag in obj.tags.all())  # Assuming the 'tags' is a Many-to-Many field

    tags_list.short_description = 'Tags'  # Optional: Custom header for this column

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Fields to display for tags in the admin panel
    search_fields = ('name',)  # Searchable fields for tags
    ordering = ('name',)  # Ordering tags alphabetically


# Registering the models with the admin site
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)

from django.contrib import admin
from django.utils import timezone
from .models import Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'category', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['status', '-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'content', 'excerpt')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at'),
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )
    
    def publish_posts(self, request, queryset):
        queryset.update(status='published', published_at=timezone.now())
    publish_posts.short_description = "Publish selected posts"
    
    actions = [publish_posts]

admin.site.register(Post, PostAdmin)

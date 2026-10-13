from django.contrib import admin

from .models import Category, Comment, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['name', 'email', 'body', 'approved']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'published_at']
    list_filter = ['status', 'category', 'published_at']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ['title']}
    raw_id_fields = ['author']
    date_hierarchy = 'published_at'
    list_editable = ['status']
    inlines = [CommentInline]

    def get_changeform_initial_data(self, request):
        return {'author': request.user.pk}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_at', 'approved']
    list_filter = ['approved', 'created_at']
    search_fields = ['name', 'email', 'body']
    actions = ['approve', 'hide']

    @admin.action(description='Approve selected comments')
    def approve(self, request, queryset):
        queryset.update(approved=True)

    @admin.action(description='Hide selected comments')
    def hide(self, request, queryset):
        queryset.update(approved=False)

from django.contrib import admin  # type: ignore

from .models import Category, Post, Location, Comment

admin.site.empty_value_display = 'Не задано'


class CommentsInline(admin.StackedInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):

    inlines = (
        CommentsInline,
    )

    list_display = (
        'title',
        'is_published',
        'category',
        'author'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('slug',)
    list_display_links = ('title',)


class CommentsAdmin(admin.ModelAdmin):

    list_display = (
        'text',
        'post',
        'created_at',
    )
    list_editable = (
        'text',
    )
    search_fields = ('author',)
    list_filter = ('post',)
    list_display_links = ('created_at',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentsAdmin)

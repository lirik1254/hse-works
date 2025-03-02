from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from news.models import NewsCategory, News, NewsComment


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(News)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_hidden', 'created_at', 'updated_at')
    list_filter = ('author', 'category', 'is_hidden')
    search_fields = ('title', 'content', 'author__username')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

    def get_readonly_fields(self, request, obj=None):
        return 'created_by', 'updated_by'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.id

        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)


@admin.register(NewsComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'is_hidden', 'created_at', 'updated_at')
    list_filter = ('is_hidden',)
    search_fields = ('content', 'author__username', 'news__title')

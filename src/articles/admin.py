from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from articles.models import ArticleTag, Article, ArticleComment


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_hidden', 'created_at', 'updated_at')
    list_filter = ('author', 'tags', 'is_hidden')
    search_fields = ('title', 'content', 'author__username')
    filter_horizontal = ('tags',)
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


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'is_hidden', 'created_at', 'updated_at')
    list_filter = ('is_hidden',)
    search_fields = ('content', 'author__username', 'article__title')

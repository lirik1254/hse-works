from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from static_pages.models import StaticPage


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_hidden', 'created_at', 'updated_at')
    list_filter = ('is_hidden',)
    search_fields = ('title', 'slug', 'content')
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

from django.contrib import admin
from .models import Section, Page


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'is_hidden')
    list_filter = ('is_hidden', 'parent')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('parent', 'title')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_sections', 'is_hidden', 'created_at')
    list_filter = ('is_hidden', 'sections')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

    def get_sections(self, obj):
        return ', '.join([section.title for section in obj.sections.all()])

    def get_readonly_fields(self, request, obj=None):
        return 'created_by', 'updated_by'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.id

        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

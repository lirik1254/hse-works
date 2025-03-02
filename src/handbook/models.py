from django.db import models
from tinymce.models import HTMLField


class Section(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.RESTRICT, related_name='subsections')
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    content = HTMLField()
    sections = models.ManyToManyField(Section, related_name='pages')
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.title

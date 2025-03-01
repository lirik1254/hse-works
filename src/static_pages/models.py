from django.db import models
from tinymce.models import HTMLField


class StaticPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    content = HTMLField()
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.title

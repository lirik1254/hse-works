from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class ArticleTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.RESTRICT)
    tags = models.ManyToManyField(ArticleTag, blank=True, related_name='articles')
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.RESTRICT)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.RESTRICT)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Article, ArticleTag, ArticleComment
from .views import ArticleListView


class ArticleListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.tag = ArticleTag.objects.create(name="Django")
        self.author = User.objects.create_user(username="testuser", password="testpass123")

        # Создаем статьи с заполненными полями created_by и updated_by
        self.article1 = Article.objects.create(
            title="Test Article 1",
            content="Content 1",
            author=self.author,
            is_hidden=False,
            created_by=self.author.id,  # Заполняем created_by
            updated_by=self.author.id  # Заполняем updated_by
        )
        self.article1.tags.add(self.tag)

        self.article2 = Article.objects.create(
            title="Another Article",
            content="Content 2",
            author=self.author,
            is_hidden=False,
            created_by=self.author.id,  # Заполняем created_by
            updated_by=self.author.id  # Заполняем updated_by
        )

        self.hidden_article = Article.objects.create(
            title="Hidden Article",
            content="Hidden Content",
            author=self.author,
            is_hidden=True,
            created_by=self.author.id,  # Заполняем created_by
            updated_by=self.author.id  # Заполняем updated_by
        )

    def test_article_list_view(self):
        """Проверка отображения списка статей."""
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_list.html')

        # Проверка, что скрытые статьи не отображаются
        self.assertNotIn(self.hidden_article, response.context['articles'])

        # Проверка сортировки статей
        articles = response.context['articles']
        self.assertEqual(articles[0], self.article2)  # Последняя статья должна быть первой
        self.assertEqual(articles[1], self.article1)

    def test_article_list_filter_by_query(self):
        """Проверка фильтрации по поисковому запросу."""
        response = self.client.get(reverse('article_list'), {'q': 'Another'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.article2, response.context['articles'])
        self.assertNotIn(self.article1, response.context['articles'])

    def test_article_list_filter_by_author(self):
        """Проверка фильтрации по автору."""
        response = self.client.get(reverse('article_list'), {'author': self.author.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.article1, response.context['articles'])
        self.assertIn(self.article2, response.context['articles'])

    def test_article_list_filter_by_tag(self):
        """Проверка фильтрации по тегу."""
        response = self.client.get(reverse('article_list'), {'tag': self.tag.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.article1, response.context['articles'])
        self.assertNotIn(self.article2, response.context['articles'])

    def test_article_list_pagination(self):
        """Проверка пагинации."""
        # Создаем больше статей для проверки пагинации
        for i in range(15):
            Article.objects.create(
                title=f"Article {i}",
                content=f"Content {i}",
                author=self.author,
                is_hidden=False,
                created_by=self.author.id,  # Заполняем created_by
                updated_by=self.author.id  # Заполняем updated_by
            )

        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['articles']), 10)

    def test_article_list_context(self):
        """Проверка контекста."""
        response = self.client.get(reverse('article_list'), {'q': 'Test', 'author': self.author.id, 'tag': self.tag.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['query'], 'Test')
        self.assertEqual(response.context['author_id'], str(self.author.id))
        self.assertEqual(response.context['tag_id'], str(self.tag.id))
        self.assertIn(self.tag, response.context['tags'])


class ArticleDetailViewTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="testuser", password="testpass123")
        self.article = Article.objects.create(
            title="Test Article",
            content="Test Content",
            author=self.author,
            is_hidden=False,
            created_by=self.author.id,  # Заполняем created_by
            updated_by=self.author.id  # Заполняем updated_by
        )
        self.hidden_article = Article.objects.create(
            title="Hidden Article",
            content="Hidden Content",
            author=self.author,
            is_hidden=True,
            created_by=self.author.id,  # Заполняем created_by
            updated_by=self.author.id  # Заполняем updated_by
        )
        self.comment1 = ArticleComment.objects.create(
            article=self.article,
            author=self.author,
            content="Comment 1",
            is_hidden=False
        )
        self.comment2 = ArticleComment.objects.create(
            article=self.article,
            author=self.author,
            content="Comment 2",
            is_hidden=False
        )
        self.hidden_comment = ArticleComment.objects.create(
            article=self.article,
            author=self.author,
            content="Hidden Comment",
            is_hidden=True
        )

    def test_article_detail_view(self):
        """Проверка отображения статьи."""
        response = self.client.get(reverse('article_detail', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_detail.html')
        self.assertEqual(response.context['article'], self.article)

    def test_hidden_article_detail_view(self):
        """Проверка, что скрытая статья не отображается."""
        response = self.client.get(reverse('article_detail', kwargs={'pk': self.hidden_article.pk}))
        self.assertEqual(response.status_code, 404)

    def test_article_detail_comments(self):
        """Проверка отображения комментариев."""
        response = self.client.get(reverse('article_detail', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        comments = response.context['comments']
        self.assertIn(self.comment1, comments)
        self.assertIn(self.comment2, comments)
        self.assertNotIn(self.hidden_comment, comments)

        # Проверка сортировки комментариев
        self.assertEqual(comments[0], self.comment2)  # Последний комментарий должен быть первым
        self.assertEqual(comments[1], self.comment1)

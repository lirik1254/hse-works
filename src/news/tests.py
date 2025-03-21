from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import News, NewsCategory, NewsComment


class NewsListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.category = NewsCategory.objects.create(name="Technology")
        self.news1 = News.objects.create(
            title="Test News 1",
            content="Content 1",
            author=self.user,
            category=self.category,
            is_hidden=False,
            created_by=self.user.id,
            updated_by=self.user.id
        )
        self.news2 = News.objects.create(
            title="Another News",
            content="Content 2",
            author=self.user,
            category=self.category,
            is_hidden=False,
            created_by=self.user.id,
            updated_by=self.user.id
        )
        self.hidden_news = News.objects.create(
            title="Hidden News",
            content="Hidden Content",
            author=self.user,
            category=self.category,
            is_hidden=True,
            created_by=self.user.id,
            updated_by=self.user.id
        )

    def test_news_list_view(self):
        """Проверка отображения списка новостей."""
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')

        # Проверка, что скрытые новости не отображаются
        self.assertNotIn(self.hidden_news, response.context['news'])

        # Проверка, что пагинация работает
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['news']), 1)  # paginate_by = 1

        # Проверка сортировки новостей
        news = response.context['news']
        self.assertEqual(news[0], self.news2)  # Последняя новость должна быть первой

    def test_news_list_filter_by_query(self):
        """Проверка фильтрации по поисковому запросу."""
        response = self.client.get(reverse('news_list'), {'q': 'Another'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.news2, response.context['news'])
        self.assertNotIn(self.news1, response.context['news'])

    def test_news_list_filter_by_author(self):
        """Проверка фильтрации по автору."""
        response = self.client.get(reverse('news_list'), {'author': self.user.id})
        self.assertEqual(response.status_code, 200)

        # Проверка, что новости отфильтрованы по автору
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 2)  # Всего новостей для автора: 2

        # Проверка, что новости присутствуют на всех страницах
        all_news = list(page_obj.paginator.object_list)  # Все новости без пагинации
        self.assertIn(self.news1, all_news)  # Первая новость
        self.assertIn(self.news2, all_news)  # Вторая новость

        # Проверка пагинации
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(page_obj.object_list), 1)  # На одной странице только 1 новость (paginate_by = 1)

    def test_news_list_filter_by_category(self):
        """Проверка фильтрации по категории."""
        response = self.client.get(reverse('news_list'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)

        # Проверка, что новости отфильтрованы по категории
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 2)  # Всего новостей для категории: 2

        # Проверка, что новости присутствуют на всех страницах
        all_news = list(page_obj.paginator.object_list)  # Все новости без пагинации
        self.assertIn(self.news1, all_news)  # Первая новость
        self.assertIn(self.news2, all_news)  # Вторая новость

        # Проверка пагинации
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(page_obj.object_list), 1)  # На одной странице только 1 новость (paginate_by = 1)

    def test_news_list_context(self):
        """Проверка контекста."""
        response = self.client.get(reverse('news_list'), {'q': 'Test', 'author': self.user.id, 'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['query'], 'Test')
        self.assertEqual(response.context['author_id'], str(self.user.id))
        self.assertEqual(response.context['category_id'], str(self.category.id))
        self.assertIn(self.category, response.context['categories'])
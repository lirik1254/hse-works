from django.test import TestCase
from django.urls import reverse
from django.views.generic import TemplateView


class HomeTemplateViewTest(TestCase):
    def test_home_template_view(self):
        """Проверка отображения главной страницы."""
        # Отправляем GET-запрос на главную страницу
        response = self.client.get(reverse('home_template'))

        # Проверяем, что статус ответа 200
        self.assertEqual(response.status_code, 200)

        # Проверяем, что используется правильный шаблон
        self.assertTemplateUsed(response, 'home/home_template.html')
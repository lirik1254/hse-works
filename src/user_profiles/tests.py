from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import UserProfile
from .forms import UserEditForm, UserProfileForm
from unittest.mock import patch
import json


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            codeforces_handle="testhandle"
        )
        self.factory = RequestFactory()

    def test_redirect_if_not_logged_in(self):
        """Проверка перенаправления неавторизованного пользователя."""
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 302)  # Проверка кода редиректа
        self.assertEqual(response.url, '/accounts/login/?next=/api/userprofile/')  # Проверка URL редиректа

    @patch('user_profiles.views.redis_client.get')
    def test_profile_view_uses_correct_template(self, mock_redis_get):
        """Проверка использования правильного шаблона."""
        # Мокируем Redis, чтобы он возвращал пустой JSON-объект
        mock_redis_get.return_value = json.dumps({})

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('user_profile'))
        self.assertTemplateUsed(response, 'user_profiles/profile.html')

    @patch('user_profiles.views.redis_client.get')
    def test_profile_view_initial_data(self, mock_redis_get):
        """Проверка инициализации форм данными пользователя."""
        # Мокируем Redis, чтобы он возвращал пустой JSON-объект
        mock_redis_get.return_value = json.dumps({})

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('user_profile'))

        # Проверка инициализации форм
        self.assertIsInstance(response.context['user_form'], UserEditForm)
        self.assertIsInstance(response.context['profile_form'], UserProfileForm)
        self.assertEqual(response.context['user_form'].instance, self.user)
        self.assertEqual(response.context['profile_form'].instance, self.profile)

    @patch('user_profiles.views.redis_client.get')
    def test_profile_view_with_codeforces_data(self, mock_redis_get):
        """Проверка передачи данных Codeforces в контекст."""
        mock_redis_get.return_value = json.dumps({'rating': 1500})  # Мокируем данные из Redis

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.context['cf_data'], {'rating': 1500})

    @patch('user_profiles.views.redis_client.get')
    def test_profile_view_without_codeforces_data(self, mock_redis_get):
        """Проверка, что данные Codeforces не передаются, если handle не указан."""
        # Устанавливаем пустую строку вместо None
        self.profile.codeforces_handle = ''
        self.profile.save()

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.context['cf_data'], {})

    def test_profile_update_valid_data(self):
        """Проверка успешного обновления профиля."""
        self.client.login(username="testuser", password="testpass123")
        data = {
            'username': 'newusername',
            'first_name': 'New',
            'last_name': 'Name',
            'bio': 'New bio',
            'university_group': 'CS-101',
            'codeforces_handle': 'newhandle'
        }
        response = self.client.post(reverse('user_profile'), data)

        # Проверка редиректа и сообщения
        self.assertRedirects(response, reverse('user_profile'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Профиль успешно сохранен.")

        # Проверка обновления данных
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.profile.codeforces_handle, 'newhandle')

    @patch('user_profiles.views.redis_client.get')
    def test_profile_update_invalid_data(self, mock_redis_get):
        """Проверка обработки невалидных данных."""
        mock_redis_get.return_value = json.dumps({})  # Мокируем пустые данные из Redis

        self.client.login(username="testuser", password="testpass123")
        data = {
            'username': 'x' * 20,  # Превышение длины
            'first_name': 'Test',
            'last_name': 'User',
            'codeforces_handle': 'invalid handle!'
        }
        response = self.client.post(reverse('user_profile'), data)

        # Проверка ошибок в формах
        self.assertFormError(response.context['user_form'], 'username',
                             'Имя пользователя не должно превышать 15 символов.')
        self.assertFormError(response.context['profile_form'], 'codeforces_handle',
                             'Codeforces handle может содержать только латинские буквы и цифры.')
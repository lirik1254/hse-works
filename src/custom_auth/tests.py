import re
from datetime import datetime, timedelta
from unittest.mock import patch

import jwt
from celery.contrib import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core import mail
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes
import pytest

from algopath import settings
from custom_auth.forms import RegistrationForm, CustomAuthenticationForm
from custom_auth.utils.confirm import generate_confirmation_link
from custom_auth.utils.token import generate_token, decode_token
from custom_auth.views import confirm_email
from user_profiles.models import UserProfile


class ConfirmationLinkTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

    def test_generate_confirmation_link(self):
        # Генерируем ссылку
        link = generate_confirmation_link(self.user)

        # Проверяем, что ссылка содержит uid и token
        uid = urlsafe_base64_encode(force_bytes(str(self.user.pk)))  # Преобразуем pk в строку
        token = default_token_generator.make_token(self.user)

        self.assertIn(uid, link)
        self.assertIn(token, link)
        self.assertTrue(link.startswith("http://127.0.0.1:8000/api/confirm-email/"))


class TokenTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "user_id": 1,
        }

    def test_generate_token(self):
        token = generate_token(self.user_data)

        self.assertIsNotNone(token)

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(payload["user_data"], self.user_data)

    def test_decode_valid_token(self):
        token = generate_token(self.user_data)

        decoded_data = decode_token(token)

        self.assertEqual(decoded_data, self.user_data)

    def test_decode_expired_token(self):
        expired_payload = {
            "user_data": self.user_data,
            "exp": datetime.utcnow() - timedelta(hours=1),  # Токен истек 1 час назад
        }
        expired_token = jwt.encode(expired_payload, settings.SECRET_KEY, algorithm="HS256")

        decoded_data = decode_token(expired_token)

        self.assertIsNone(decoded_data)

    def test_decode_invalid_token(self):
        invalid_token = jwt.encode(self.user_data, "wrong_secret_key", algorithm="HS256")

        decoded_data = decode_token(invalid_token)

        self.assertIsNone(decoded_data)


class RegistrationFormTest(TestCase):
    def test_clean_email_unique(self):
        User.objects.create_user(username='test', email='test@example.com')
        form = RegistrationForm(data={'email': 'test@example.com'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_clean_username_unique(self):
        User.objects.create_user(username='testuser')
        form = RegistrationForm(data={'username': 'testuser'})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_clean_codeforces_handle_validation(self):
        form = RegistrationForm(data={'codeforces_handle': 'invalid_handle'})
        form.is_valid()
        self.assertIn('codeforces_handle', form.errors)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'university_group': 'CS-101'
        }

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_confirm_email_with_invalid_token(self):
        invalid_token = 'invalid_token'
        uid = urlsafe_base64_encode(force_bytes('test@example.com'))
        url = reverse('confirm_email', kwargs={'uidb64': uid, 'token': invalid_token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ссылка недействительна', response.content.decode())


class RegisterViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'university_group': 'CS-101',
            'codeforces_handle': 'test_handle'
        }

    def test_register_get_request(self):
        """Проверка GET-запроса: форма должна отображаться."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegistrationForm)
        self.assertTemplateUsed(response, 'custom_auth/register.html')

    @patch('codeforces.service.get_user_dict')  # Мокируем вызов Codeforces API
    def test_register_post_valid_data(self, mock_get_user):
        """Проверка POST-запроса с валидными данными."""
        # Настраиваем мок для Codeforces API
        mock_get_user.return_value = {'status': 'OK', 'rating': 1500}

        # Отправляем POST-запрос с валидными данными
        response = self.client.post(reverse('register'), data=self.user_data)

        # Проверяем, что произошёл редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

        # Проверяем, что письмо отправлено
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Подтверждение регистрации")
        self.assertIn(self.user_data['username'], email.body)

        # Проверяем сообщение об успешной отправке письма
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Письмо с подтверждением отправлено. Проверьте почту.")

    def test_register_post_invalid_data(self):
        """Проверка POST-запроса с невалидными данными."""
        # Отправляем POST-запрос с невалидными данными (без email)
        invalid_data = self.user_data.copy()
        invalid_data.pop('email')

        response = self.client.post(reverse('register'), data=invalid_data)

        # Проверяем, что форма не прошла валидацию
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

        # Проверяем, что ошибка отображается
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Ошибка в данных формы.")

    @patch('codeforces.service.get_user_dict')
    def test_register_post_existing_email(self, mock_get_user):
        """Проверка POST-запроса с уже зарегистрированным email."""
        # Создаем пользователя с таким же email
        User.objects.create_user(username='existing_user', email='test@example.com')

        # Настраиваем мок для Codeforces API
        mock_get_user.return_value = {'status': 'OK', 'rating': 1500}

        # Отправляем POST-запрос с уже зарегистрированным email
        response = self.client.post(reverse('register'), data=self.user_data)

        # Проверяем, что форма не прошла валидацию
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

        # Проверяем, что ошибка отображается
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Ошибка в данных формы.")


class ConfirmEmailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Testpass123!",
            "first_name": "Test",
            "last_name": "User",
            "university_group": "CS-101",
            "codeforces_handle": "test_handle"
        }

    def test_confirm_email_success(self):
        """Проверка успешного подтверждения email."""
        # Генерируем токен и uidb64
        token = generate_token(self.user_data)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user_data["email"]))

        # Создаем запрос
        request = self.factory.get(reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token}))
        request.session = {}

        # Настраиваем messages для request
        messages = FallbackStorage(request)
        request._messages = messages

        # Вызываем метод confirm_email
        with patch('codeforces.service.get_user_dict') as mock_get_user:
            mock_get_user.return_value = {'rating': 1500}
            response = confirm_email(request, uidb64, token)

        # Проверяем, что произошёл редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

        # Проверяем, что пользователь создан
        user = User.objects.get(username=self.user_data["username"])
        self.assertEqual(user.email, self.user_data["email"])

        # Проверяем, что профиль пользователя создан
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.university_group, self.user_data["university_group"])
        self.assertEqual(profile.codeforces_handle, self.user_data["codeforces_handle"])

        # Проверяем сообщение об успешной регистрации
        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Регистрация подтверждена! Теперь вы можете войти.")

    def test_confirm_email_invalid_token(self):
        """Проверка недействительного токена."""
        # Генерируем uidb64
        uidb64 = urlsafe_base64_encode(force_bytes(self.user_data["email"]))

        # Создаем запрос с недействительным токеном
        request = self.factory.get(reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': 'invalid_token'}))
        request.session = {}

        # Настраиваем messages для request
        messages = FallbackStorage(request)
        request._messages = messages

        response = confirm_email(request, uidb64, 'invalid_token')

        # Проверяем, что возвращается ошибка
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Ссылка недействительна.")


class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Testpass123!'
        )

    def test_custom_login_get_request(self):
        """Проверка GET-запроса: форма должна отображаться."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)
        self.assertTemplateUsed(response, 'custom_auth/login.html')

    def test_custom_login_post_valid_username(self):
        """Проверка POST-запроса с валидным username."""
        # Отправляем POST-запрос с валидными данными (username)
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Testpass123!'
        })

        # Проверяем, что произошёл редирект на главную страницу
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home_template'))

    def test_custom_login_post_valid_email(self):
        """Проверка POST-запроса с валидным email."""
        # Отправляем POST-запрос с валидными данными (email)
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'Testpass123!'
        })

        # Проверяем, что произошёл редирект на главную страницу
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home_template'))

    def test_custom_login_post_invalid_username(self):
        """Проверка POST-запроса с неверным username."""
        # Отправляем POST-запрос с неверным username
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'Testpass123!'
        })


        # Проверяем, что отображается ошибка
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Пользователь не зарегистрирован или email не подтвержден")

    def test_custom_login_post_invalid_email(self):
        """Проверка POST-запроса с неверным email."""
        # Отправляем POST-запрос с неверным email
        response = self.client.post(reverse('login'), {
            'username': 'wrong@example.com',
            'password': 'Testpass123!'
        })


        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Пользователь не зарегистрирован или email не подтвержден")

    def test_custom_login_post_invalid_password(self):
        """Проверка POST-запроса с неверным паролем."""
        # Отправляем POST-запрос с неверным паролем
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })


        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Неверный логин или пароль.")

    def test_custom_login_post_unregistered_user(self):
        """Проверка POST-запроса для незарегистрированного пользователя."""
        # Отправляем POST-запрос для незарегистрированного пользователя
        response = self.client.post(reverse('login'), {
            'username': 'unregistereduser',
            'password': 'Testpass123!'
        })


        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Пользователь не зарегистрирован или email не подтвержден")
# your_app/tests/test_utils.py
import json
import os
import re
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.test import TestCase, RequestFactory
import responses
from dotenv import load_dotenv

from user_profiles.models import UserProfile
from .client import get_user_info
from .service import get_user_dict
from unittest.mock import patch
from .utils.output_utils import pluralize_days, pluralize_hours
from .utils.time_utils import get_last_seen_time, get_registration_time
from .views import codeforces_user_info, participants


class UserInfoTests(TestCase):
    @responses.activate
    def test_get_user_info(self):
        mock_response = {
            "status": "OK",
            "result": [
                {
                    "handle": "test_user",
                    "rating": 1500,
                    "maxRating": 1600,
                    "friendOfCount": 10,
                    "titlePhoto": "https://example.com/photo.jpg",
                    "organization": "Test Org",
                    "rank": "expert",
                    "maxRank": "master",
                    "lastOnlineTimeSeconds": 1672502400,
                    "registrationTimeSeconds": 1640995200
                }
            ]
        }

        responses.add(
            responses.GET,
            "https://codeforces.com/api/user.info?handles=test_user&checkHistoricHandles=false",
            json=mock_response,
            status=200
        )

        result = get_user_info("test_user")
        self.assertEqual(result, mock_response)

    @responses.activate
    @patch("codeforces.service.get_last_seen_time")
    def test_get_user_dict(self, mock_get_last_seen_time):
        # Фиксируем возвращаемое значение для get_last_seen_time
        mock_get_last_seen_time.return_value = "Был в сети  9 дней 0 часов назад"

        # Мок ответа от API
        mock_response = {
            "status": "OK",
            "result": [
                {
                    "handle": "test_user",
                    "rating": 1500,
                    "maxRating": 1600,
                    "friendOfCount": 10,
                    "titlePhoto": "https://example.com/photo.jpg",
                    "organization": "Test Org",
                    "rank": "expert",
                    "maxRank": "master",
                    "lastOnlineTimeSeconds": 1672502400,  # 1 января 2023 года, 00:00:00
                    "registrationTimeSeconds": 1640995200  # 1 января 2022 года, 00:00:00
                }
            ]
        }

        responses.add(
            responses.GET,
            "https://codeforces.com/api/user.info?handles=test_user&checkHistoricHandles=false",
            json=mock_response,
            status=200
        )

        # Вызов тестируемой функции
        result = get_user_dict("test_user")

        # Ожидаемый результат
        expected_dict = {
            "rating": 1500,
            "max_rating": 1600,
            "friend_count": 10,
            "title_photo": "https://example.com/photo.jpg",
            "organization": "Test Org",
            "rank": "expert",
            "max_rank": "master",
            "last_online_time": "Был в сети  9 дней 0 часов назад",  # Фиксированное значение
            "registration_date": "01-01-2022 05:00"  # Формат из вашего примера
        }

        # Проверка результата
        self.assertEqual(result, expected_dict)


class TimeUtils(TestCase):
    @patch("codeforces.utils.time_utils.datetime")
    def test_get_last_seen_time_less_than_a_day(self, mock_datetime):
        fixed_now = datetime(2023, 10, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        last_online_time = int((fixed_now - timedelta(hours=2)).timestamp())
        expected_result = "Был в сети 2 часа назад"
        result = get_last_seen_time(last_online_time)
        self.assertEqual(result, expected_result)

    @patch("codeforces.utils.time_utils.datetime")
    def test_get_last_seen_time_more_than_a_day(self, mock_datetime):
        fixed_now = datetime(2023, 10, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        last_online_time = int((fixed_now - timedelta(days=2)).timestamp())
        expected_result = "Был в сети  2 дня 0 часов назад"
        result = get_last_seen_time(last_online_time)
        self.assertEqual(result, expected_result)

    @patch("codeforces.utils.time_utils.datetime")
    def test_get_last_seen_time_exactly_one_day(self, mock_datetime):
        fixed_now = datetime(2023, 10, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        last_online_time = int((fixed_now - timedelta(days=1)).timestamp())
        expected_result = "Был в сети  1 день 0 часов назад"
        result = get_last_seen_time(last_online_time)
        self.assertEqual(result, expected_result)

    def test_get_registration_time(self):
        registration_time = 1640995200  # 1 января 2022 года, 00:00:00
        expected_result = "01-01-2022 05:00"
        result = get_registration_time(registration_time)
        self.assertEqual(result, expected_result)

    def test_get_registration_time_with_time(self):
        registration_time = 1678883400  # 15 марта 2023 года, 14:30:00
        expected_result = "15-03-2023 17:30"
        result = get_registration_time(registration_time)
        self.assertEqual(result, expected_result)


class TestPluralizeDays(TestCase):

    def test_pluralize_days_one(self):
        result = pluralize_days(1)
        self.assertEqual(result, "1 день")

    def test_pluralize_days_two(self):
        result = pluralize_days(2)
        self.assertEqual(result, "2 дня")

    def test_pluralize_days_five(self):
        result = pluralize_days(5)
        self.assertEqual(result, "5 дней")


class TestPluralizeHours(TestCase):

    def test_pluralize_hours_one(self):
        result = pluralize_hours(1)
        self.assertEqual(result, "1 час")

    def test_pluralize_hours_two(self):
        result = pluralize_hours(2)
        self.assertEqual(result, "2 часа")

    def test_pluralize_hours_five(self):
        result = pluralize_hours(5)
        self.assertEqual(result, "5 часов")


class TestCodeforcesUserInfo(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            password="testpass123"
        )
        self.factory = RequestFactory()

    def test_user_not_found(self):
        # Создаем запрос с несуществующим именем пользователя
        request = self.factory.get("/api/codeforces/participants/non_existent_user/")
        request.user = self.user

        # Проверяем, что вызывается Http404
        with self.assertRaises(Http404) as context:
            codeforces_user_info(request, "non_existent_user")

        # Проверяем сообщение об ошибке
        self.assertEqual(str(context.exception), "Пользователь не найден")

    def test_user_without_profile(self):
        # Создаем запрос с существующим именем пользователя
        request = self.factory.get(f"/api/codeforces/participants/{self.user.username}/")
        request.user = self.user

        # Убедимся, что у пользователя нет профиля
        self.assertFalse(hasattr(self.user, 'userprofile'))

        # Вызываем функцию
        response = codeforces_user_info(request, self.user.username)

        # Парсим HTML-контент
        soup = BeautifulSoup(response.content, "html.parser")

        # Ищем все элементы <p>
        all_p_tags = soup.find_all("p")

        # Создаем словарь для хранения данных
        user_data = {}

        # Обрабатываем каждый <p>
        for p_tag in all_p_tags:
            text = p_tag.get_text(strip=True)
            if "Имя:" in text:
                user_data["Имя"] = text.replace("Имя:", "").strip()
            elif "Фамилия:" in text:
                user_data["Фамилия"] = text.replace("Фамилия:", "").strip()
            elif "Дата регистрации:" in text:
                user_data["Дата регистрации"] = text.replace("Дата регистрации:", "").strip()
            elif "Последний вход:" in text:
                user_data["Последний вход"] = text.replace("Последний вход:", "").strip()
            elif "Биография:" in text:
                user_data["Биография"] = text.replace("Биография:", "").strip()
            elif "Группа университета:" in text:
                user_data["Группа университета"] = text.replace("Группа университета:", "").strip()

        # Проверяем, что данные пользователя корректны
        self.assertEqual(user_data["Имя"], "Test")
        self.assertEqual(user_data["Фамилия"], "User")
        self.assertIsNotNone(user_data["Дата регистрации"])
        self.assertEqual(user_data["Последний вход"], "-")
        self.assertEqual(user_data["Биография"], "-")
        self.assertEqual(user_data["Группа университета"], "-")

        # Проверяем информацию о Codeforces
        codeforces_info = soup.find("p", text=lambda x: x and "Информация о пользователе на Codeforces" in x).get_text(
            strip=True)
        self.assertEqual(codeforces_info, "Информация о пользователе на Codeforces не найдена.")

    def test_user_with_profile_and_codeforces(self):
        # Создаем профиль для пользователя с хэндлом Codeforces
        UserProfile.objects.create(
            user=self.user,
            bio="Test Bio",
            university_group="Group 1",
            codeforces_handle="test_handle"
        )

        # Мокируем Redis, чтобы вернуть фиктивные данные
        fake_redis_data = json.dumps({"rating": 1500})
        with patch('custom_auth.tasks.redis_client.get', return_value=fake_redis_data):
            # Создаем запрос
            request = self.factory.get(f"/api/codeforces/participants/{self.user.username}/")
            request.user = self.user

            # Вызываем функцию
            response = codeforces_user_info(request, self.user.username)

            # Парсим HTML-контент
            soup = BeautifulSoup(response.content, "html.parser")

            # Проверяем, что данные профиля отображаются
            self.assertIn("Test Bio", soup.get_text())
            self.assertIn("Group 1", soup.get_text())

            # Проверяем, что данные Codeforces отображаются
            self.assertIn("1500", soup.get_text())  # Рейтинг

    def test_participants(self):
        # Создаем несколько пользователей с профилями
        user1 = User.objects.create_user(username="user1", first_name="User1", last_name="Test")
        user2 = User.objects.create_user(username="user2", first_name="User2", last_name="Test")
        UserProfile.objects.create(user=user1, codeforces_handle="handle1")
        UserProfile.objects.create(user=user2, codeforces_handle="handle2")

        # Мокируем Redis, чтобы вернуть фиктивные данные
        fake_redis_data_handle1 = json.dumps({"rating": 1600})
        fake_redis_data_handle2 = json.dumps({"rating": 1400})
        with patch('custom_auth.tasks.redis_client.get',
                   side_effect=[fake_redis_data_handle1, fake_redis_data_handle2]):
            # Создаем запрос
            request = self.factory.get("/api/codeforces/participants/")
            request.user = self.user

            # Вызываем функцию
            response = participants(request)

            # Проверяем, что ответ содержит данные о пользователях
            self.assertIn("user1", response.content.decode())
            self.assertIn("user2", response.content.decode())
            self.assertIn("1600", response.content.decode())
            self.assertIn("1400", response.content.decode())

            # Проверяем, что пользователи отсортированы по рейтингу
            soup = BeautifulSoup(response.content, "html.parser")
            # Находим все элементы <li>
            all_li_tags = soup.find_all("li")

            # Создаем список для хранения рейтингов
            ratings = []

            # Обрабатываем каждый <li>
            for li_tag in all_li_tags:
                text = li_tag.get_text(strip=True)
                match = re.search(r"Рейтинг:\s*(\d+|Не доступен)", text)
                if match:
                    ratings.append(match.group(1))

            # Проверяем, что рейтинги корректны
            self.assertIn("1600", ratings)
            self.assertIn("1400", ratings)
            self.assertIn("Не доступен", ratings)
import jwt
from django.conf import settings
from datetime import datetime, timedelta

SECRET_KEY = settings.SECRET_KEY  # Берем секретный ключ Django


def generate_token(data):
    """Создает токен с данными пользователя (не в БД)"""
    payload = {
        "user_data": data,
        "exp": datetime.utcnow() + timedelta(hours=24),  # Токен истекает через 24 часа
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token):
    """Декодирует токен и возвращает данные пользователя"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_data"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

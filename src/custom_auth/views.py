import json
import re

from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetDoneView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.urls import reverse

from django.conf import settings
from django.utils.encoding import force_bytes, force_str

from .forms import RegistrationForm, CustomAuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from user_profiles.models import UserProfile
from django.contrib.auth.models import User
from codeforces.service import get_user_dict
import redis
from .tasks import refresh_cf_data

from .utils.token import generate_token, decode_token

redis_client = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"], decode_responses=True)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_data = form.get_user_data()  # Получаем данные без сохранения в БД

            # Генерируем токен с данными пользователя
            token = generate_token(user_data)

            # Формируем ссылку подтверждения
            uidb64 = urlsafe_base64_encode(force_bytes(user_data["email"]))
            confirmation_link = request.build_absolute_uri(
                reverse("confirm_email", kwargs={"uidb64": uidb64, "token": token})
            )

            # Отправляем письмо с подтверждением
            subject = "Подтверждение регистрации"
            message = (f"Привет, {user_data['username']}\n\n"
                       f"Благодарим вас за регистрацию на сайте факультета спортивного"
                       f" программирования г. Перми!\n\n"
                       f"Для того, чтобы попасть на сайт, подтвердите регистрацию:\n{confirmation_link}\n\n"
                       f"С уважением, команда ФСП")
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_data["email"]])

            messages.success(request, "Письмо с подтверждением отправлено. Проверьте почту.")
            return redirect("login")

        else:
            messages.error(request, "Ошибка в данных формы.")
    else:
        form = RegistrationForm()

    return render(request, "custom_auth/register.html", {"form": form})


def confirm_email(request, uidb64, token):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        return HttpResponse("Ошибка в ссылке подтверждения.")

    user_data = decode_token(token)
    if not user_data or user_data["email"] != email:
        return HttpResponse("Ссылка недействительна.")

    # Создаем пользователя
    user = User.objects.create_user(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"]
    )
    print(user)

    # Создаем профиль пользователя
    UserProfile.objects.create(
        user=user,
        university_group=user_data["university_group"],
        codeforces_handle=user_data["codeforces_handle"],
    )

    handle = user_data['codeforces_handle']
    if handle:
        redis_client.set(handle, json.dumps(get_user_dict(handle)))
        task = refresh_cf_data.apply_async((handle,), countdown=86400)
        redis_client.set(f"cf_task_{handle}", task.id)

    messages.success(request, "Регистрация подтверждена! Теперь вы можете войти.")
    return redirect("login")


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data.get('username')  # Может быть email или username
            password = form.cleaned_data.get('password')
            # Проверяем, является ли введённое значение email'ом
            if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
                try:
                    user = User.objects.get(email=identifier)
                    username = user.username  # Используем username для аутентификации
                except User.DoesNotExist:
                    messages.error(request, "Пользователь не зарегистрирован или email не подтвержден")
                    return redirect('login')
            else:
                username = identifier  # Используем введённый username

            # Проверяем, существует ли пользователь в БД
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "Пользователь не зарегистрирован или email не подтвержден")
                return redirect('login')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home_template')
            else:
                messages.error(request, "Неверный логин или пароль.")
                return redirect('login')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'custom_auth/login.html', {'form': form})


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "Регистрация подтверждена! Теперь вы можете войти.")
        return redirect('login')  #


class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "Письмо с подтверждением отправлено. Проверьте почту.")
        # Редиректим пользователя на страницу логина после того, как email был отправлен
        return redirect('login')  # Указываем URL для страницы логина

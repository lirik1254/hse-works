from .forms import RegistrationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from user_profiles.models import UserProfile
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request=request)  # Сохраняем пользователя и профиль
            messages.success(request, 'Подтвердите почту')
            return redirect('login')  # Перенаправляем на страницу входа (или другую)
        else:
            messages.error(request, 'Ошибка в данных формы.')
    else:
        form = RegistrationForm()

    return render(request, 'custom_auth/register.html', {'form': form})


def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        user.userprofile.email_confirmed = True
        user.userprofile.save()

        messages.success(request, "Почта успешно подтверждена.")
        return redirect('login')
    else:
        return HttpResponse("Ссылка недействительна или устарела.")


def custom_login(request):
    if request.method == 'POST':
        # Сначала пытаемся аутентифицировать пользователя по данным из POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Пытаемся аутентифицировать пользователя
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"User {username} authenticated successfully.")
            # Теперь создаем форму и проверяем ее на валидность
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                # Если форма валидна, проверяем профиль пользователя
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    print(user_profile)
                    if user_profile.email_confirmed:
                        login(request, user)
                        return redirect('home')  # Редирект на главную страницу
                    else:
                        messages.error(request, "Пожалуйста, подтвердите ваш email.")
                        return redirect('login')  # Страница логина
                except UserProfile.DoesNotExist:
                    messages.error(request, "Профиль пользователя не найден.")
                    return redirect('login')  # Страница логина
            else:
                print(form.errors)
                messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
                return redirect('login')  # Страница логина
        else:
            # Если аутентификация не удалась, выводим ошибку
            print("Authentication failed.")
            messages.error(request, "Неверный логин или пароль.")
            return redirect('login')  # Страница логина

    else:
        form = AuthenticationForm()

    return render(request, 'custom_auth/login.html', {'form': form})


def home(request):
    user = User.objects.get(username='test')  # Замените на актуальное имя пользователя
    print(user.check_password('kukukuku'))
    return render(request, 'custom_auth/home.html')

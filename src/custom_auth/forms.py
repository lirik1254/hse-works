from django.contrib.auth.forms import UserCreationForm
from user_profiles.models import UserProfile
from django.core.mail import send_mail
from django.conf import settings
from .utils.token import generate_confirmation_link
import socket
from django import forms
from django.contrib.auth.models import User

socket.getfqdn = lambda *args: "localhost"


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    university_group = forms.CharField(max_length=16, required=True)
    codeforces_handle = forms.CharField(max_length=24, required=False)
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True, request=None):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False

        if commit:
            user.save()

            # Создаем профиль пользователя
            profile = UserProfile.objects.create(
                user=user,
                university_group=self.cleaned_data['university_group'],
                codeforces_handle=self.cleaned_data.get('codeforces_handle'),
            )
            profile.save()

            # Создаем и отправляем токен подтверждения на почту
            confirmation_link = generate_confirmation_link(user)
            subject = "Подтверждение регистрации"
            message = (f"Привет, {user.username}!\n\nПожалуйста, подтвердите вашу почту,"
                       f" перейдя по ссылке:\n{confirmation_link}")
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user



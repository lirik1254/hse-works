import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user_profiles.models import UserProfile
import socket
from django import forms
from django.contrib.auth.models import User
from codeforces.client import get_user_info

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

    def clean_email(self):
        """Проверка уникальности email."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean_username(self):
        """Проверка уникальности ника."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Этот ник уже занят.")
        return username

    def clean_codeforces_handle(self):
        """Проверка уникальности Codeforces handle."""
        codeforces_handle = self.cleaned_data.get('codeforces_handle')
        if codeforces_handle and UserProfile.objects.filter(codeforces_handle=codeforces_handle).exists():
            raise forms.ValidationError("Этот Codeforces handle уже зарегистрирован в системе")
        if get_user_info(codeforces_handle)['status'] == 'FAILED':
            raise forms.ValidationError("Такой аккаунт не зарегистрирован на codeforces")
        return codeforces_handle

    def get_user_data(self):
        """Возвращает данные пользователя без сохранения в БД"""
        return {
            "username": self.cleaned_data["username"],
            "email": self.cleaned_data["email"],
            "password": self.cleaned_data["password1"],  # Пароль зашифруем позже
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "university_group": self.cleaned_data["university_group"],
            "codeforces_handle": self.cleaned_data.get("codeforces_handle"),
        }


class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя или Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя или email'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )

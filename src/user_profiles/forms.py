import json
import re
import time

from django import forms
from django.contrib.auth.models import User

from codeforces.client import get_user_info
from codeforces.service import get_user_dict
from .models import UserProfile
from custom_auth.tasks import redis_client, refresh_cf_data
from django.core.exceptions import ValidationError


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "maxlength": "15"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "maxlength": "25"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "maxlength": "25"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 15:
            raise ValidationError('Имя пользователя не должно превышать 15 символов.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 25:
            raise ValidationError('Имя не должно превышать 25 символов.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 25:
            raise ValidationError('Фамилия не должна превышать 25 символов.')
        return last_name


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "university_group", "codeforces_handle"]
        labels = {
            "bio": "Биография",
            "university_group": "Учебная группа",
            "codeforces_handle": "Ник codeforces",
        }
    def clean_codeforces_handle(self):
        """Проверка уникальности Codeforces handle и существования аккаунта."""
        codeforces_handle = self.cleaned_data.get("codeforces_handle")
        if self.has_changed() and "codeforces_handle" in self.changed_data:
            if not codeforces_handle:
                return codeforces_handle
            if not re.match(r'^[A-Za-z0-9]+$', codeforces_handle):
                raise ValidationError('Codeforces handle может содержать только латинские буквы и цифры.')

            # Проверка уникальности, исключая текущего пользователя
            if UserProfile.objects.filter(codeforces_handle=codeforces_handle).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Этот Codeforces handle уже зарегистрирован в системе")

            if get_user_info(codeforces_handle)["status"] == "FAILED":
                raise forms.ValidationError("Такой аккаунт не зарегистрирован на Codeforces")

        return codeforces_handle

    def save(self, commit=True):
        """Сохранение профиля, обновление данных в Redis и отмена старых задач."""
        instance = super().save(commit=False)

        if self.has_changed() and "codeforces_handle" in self.changed_data:
            old_handle = self.initial.get("codeforces_handle")  # Получаем старое значение
            new_handle = instance.codeforces_handle
                # Удаляем старый handle из Redis
            if old_handle:
                redis_client.delete(old_handle)  # Удаление из Redis

            # Если новый handle указан, обновляем Redis и ставим задачу на обновление
            if new_handle:
                redis_client.set(new_handle, json.dumps(get_user_dict(new_handle)))
                task = refresh_cf_data.apply_async((new_handle,), countdown=86400)

                # Сохраняем ID задачи в Redis, чтобы потом её отменять
                redis_client.set(f"cf_task_{new_handle}", task.id)

            # Удаляем старую задачу обновления
            if old_handle:
                old_task_id = redis_client.get(f"cf_task_{old_handle}")
                if old_task_id:
                    refresh_cf_data.AsyncResult(old_task_id).revoke(terminate=True)  # Отмена старой задачи
                    redis_client.delete(f"cf_task_{old_handle}")  # Удаление ссылки на старую задачу

        if commit:
            instance.save()
        return instance


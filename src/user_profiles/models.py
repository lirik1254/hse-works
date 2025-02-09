from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(1000, message="Максимальная длина биографии 1000 символов.")]
    )
    university_group = models.CharField(max_length=16, null=True, blank=True)
    codeforces_handle = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

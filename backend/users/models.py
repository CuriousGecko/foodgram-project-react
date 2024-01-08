from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from foodgram_backend.constants import (MAX_LENGHT_EMAIL, MAX_LENGHT_LAST_NAME,
                                        MAX_LENGTH_FIRST_NAME)


class CustomUser(AbstractUser):
    """Переопределенная модель пользователя."""

    email = models.EmailField(
        'Электронная почта',
        max_length=MAX_LENGHT_EMAIL,
        unique=True,
        error_messages={
            'unique': 'Пользователь с такой электронной почтой уже существует.'
        },
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH_FIRST_NAME,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGHT_LAST_NAME,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def clean(self):
        if self.username.lower() == 'me':
            raise ValidationError(
                'Имя пользователя не может быть "me".'
            )

from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Пользователь, который подписывается.'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь, на которого подписываемся.'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow',
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

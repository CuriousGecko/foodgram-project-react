from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Пользователь, который подписывается.'
    )
    author = models.ForeignKey(
        User,
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
        return f'{self.user} подписан на {self.author}.'

    def clean(self):
        if self.user == self.author:
            raise ValidationError(
                'Нельзя создать подписку на самого себя.'
            )

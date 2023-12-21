from rest_framework import status
from rest_framework.exceptions import ValidationError

from users.models import Subscription


def validate_is_subscribed(self, author):
    user = self.context.get('request').user
    author = author
    if Subscription.objects.filter(
            user=user,
            author=author,
    ).exists():
        raise ValidationError(
            detail='Подписка на данного пользователя уже существует.',
            code=status.HTTP_400_BAD_REQUEST,
        )
    if user == author:
        raise ValidationError(
            detail='Подписаться на самого себя нельзя.',
            code=status.HTTP_400_BAD_REQUEST,
        )
    return True
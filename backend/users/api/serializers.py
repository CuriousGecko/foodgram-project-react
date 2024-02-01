from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoUserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from subscriptions.models import Subscription

User = get_user_model()


class UserCreateSerializer(DjoUserCreateSerializer):
    class Meta:
        model = User
        fields = (
            (User.USERNAME_FIELD, 'password', 'id',)
            + tuple(User.REQUIRED_FIELDS)
        )

    def validate_username(self, username):
        if username.lower() == 'me':
            raise ValidationError(
                "Имя пользователя не может быть 'me'."
            )
        return username


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            (User.USERNAME_FIELD, 'id',)
            + tuple(User.REQUIRED_FIELDS)
            + ('is_subscribed',)
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and obj.following.filter(user=request.user).exists()
        )

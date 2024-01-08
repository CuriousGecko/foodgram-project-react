from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from subscriptions.models import Subscription

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            (User.USERNAME_FIELD, 'password', 'id',)
            + tuple(User.REQUIRED_FIELDS)
        )


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            (User.USERNAME_FIELD, 'id',)
            + tuple(User.REQUIRED_FIELDS)
            + ('is_subscribed',)
        )

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Subscription.objects.filter(
                user=self.context.get('request').user,
                author=obj,
            ).exists()
        )

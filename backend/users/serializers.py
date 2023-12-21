from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from recipes.models import Recipe
from users.models import Subscription

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
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(
            user=request.user,
            author=obj,
        ).exists()


class UserSubscribesSerializer(CustomUserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            CustomUserSerializer.Meta.fields
            + ('recipes', 'recipes_count',)
        )
        read_only_fields = (
            tuple(User.REQUIRED_FIELDS)
            + (User.USERNAME_FIELD,)
        )

    def get_recipes_count(self, author):
        return author.recipes.count()

    def get_recipes(self, author):
        limit = self.context.get('request').GET.get('recipes_limit')
        recipes = author.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortVersionSerializer(
            recipes,
            many=True,
            read_only=True,
        )
        return serializer.data

    def validate(self, data):
        user = self.context.get('request').user
        author = self.instance
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
        return data


class RecipeShortVersionSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

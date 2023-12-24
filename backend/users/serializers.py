from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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


class SubscriptionListSerializer(CustomUserSerializer):
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
        limit = self.context.get('request').query_params.get('recipes_limit')
        recipes = author.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortVersionSerializer(
            recipes,
            many=True,
            read_only=True,
        )
        return serializer.data


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'user',
            'author',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Подписка на данного пользователя уже существует.',
            )
        ]

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(
                'Подписаться на самого себя нельзя.'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscriptionListSerializer(
            instance,
            context={'request': request},
        ).data


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

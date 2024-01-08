from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.api.serializers import RecipeShortSerializer
from subscriptions.models import Subscription
from users.api.serializers import CustomUserSerializer

User = get_user_model()


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
        serializer = RecipeShortSerializer(
            recipes,
            many=True,
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
        return SubscriptionListSerializer(
            instance=self.context.get('author'),
            context={'request': self.context.get('request')},
        ).data

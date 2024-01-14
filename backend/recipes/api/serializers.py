from django.db import transaction
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from favorite.models import Favorite
from foodgram_backend.constants import MIN_AMOUNT
from ingredients.api.serializers import (IngredientCreateSerializer,
                                         RecipeIngredientsSerializer)
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredients
from shoppingcart.models import ShoppingCart
from tags.api.serializers import TagSerializer
from users.api.serializers import UserSerializer


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True,
    )
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, recipe):
        return RecipeIngredientsSerializer(
            RecipeIngredients.objects.filter(recipe=recipe),
            many=True,
        ).data

    def get_is_favorited(self, recipe):
        return self.check_is(recipe, Favorite)

    def get_is_in_shopping_cart(self, recipe):
        return self.check_is(recipe, ShoppingCart)

    def check_is(self, recipe, model):
        user = self.context.get('request').user
        return user.is_authenticated and model.objects.filter(
            user=user.id,
            recipe=recipe.id,
        ).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True,
    )
    ingredients = IngredientCreateSerializer(
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'id',
        )

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Нужно добавить в рецепт хотя бы один ингредиент.'
            )
        ingredients_list = []
        for element in ingredients:
            try:
                ingredient = Ingredient.objects.get(
                    id=element.get('id'),
                )
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    'Нельзя добавить в рецепт отсутствующий в БД ингредиент.'
                )
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Обнаружены дубликаты ингредиентов.'
                )
            ingredients_list.append(ingredient)
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                'Нужно указать хотя бы один тег.'
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Обнаружены дубликаты тегов.'
                )
            tags_list.append(tag)
        return tags

    def validate_name(self, name):
        if not any(char.isalpha() for char in name):
            raise serializers.ValidationError(
                'В названии рецепта должны присутствовать буквы.'
            )
        return name

    def validate(self, data):
        if 'tags' not in data:
            raise serializers.ValidationError(
                {'tags': ['Требуется указать данное поле.']},
            )
        if 'ingredients' not in data:
            raise serializers.ValidationError(
                {'ingredients': ['Требуется указать данное поле.']},
            )
        return data

    @transaction.atomic
    def create_ingredients_amounts(self, ingredients, recipe):
        RecipeIngredients.objects.bulk_create(
            RecipeIngredients(
                ingredient=Ingredient.objects.get(id=ingredient.get('id')),
                recipe=recipe,
                amount=ingredient.get('amount'),
            ) for ingredient in ingredients
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_amounts(
            recipe=recipe,
            ingredients=ingredients,
        )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(
            instance,
            validated_data,
        )
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_amounts(
            recipe=instance,
            ingredients=ingredients,
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeReadSerializer(
            instance,
            context={'request': request},
        ).data


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

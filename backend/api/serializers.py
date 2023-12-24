from django.db import transaction
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                            ShoppingCart, Tag)
from users.serializers import (CustomUserSerializer,
                               RecipeShortVersionSerializer)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        read_only_fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        read_only_fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id',
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        validators = (
            UniqueTogetherValidator(
                queryset=RecipeIngredients.objects.all(),
                fields=(
                    'ingredient',
                    'recipe',
                )
            ),
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
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
        if not user.is_authenticated:
            return False
        return model.objects.filter(
            user=user.id,
            recipe=recipe.id,
        ).exists()


class IngredientCreateSerializer(serializers.ModelSerializer):
    id = IntegerField(
        write_only=True,
    )

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
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
            ingredient = Ingredient.objects.filter(
                id=element.get('id'),
            ).first()
            if not ingredient:
                raise serializers.ValidationError(
                    'Нельзя добавить в рецепт отсутствующий в БД ингредиент.'
                )
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Обнаружены дубликаты ингредиентов.'
                )
            if int(element.get('amount')) <= 0:
                raise serializers.ValidationError(
                    'Не указано количество ингредиента.'
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
            [
                RecipeIngredients(
                    ingredient=Ingredient.objects.get(id=ingredient.get('id')),
                    recipe=recipe,
                    amount=ingredient.get('amount'),
                ) for ingredient in ingredients
            ]
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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        if Favorite.objects.filter(
            user=data.get('user'),
            recipe=data.get('recipe'),
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже в избранном.'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortVersionSerializer(
            instance.recipe,
        ).data


class ShoppingCartSerializer(FavoriteSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        if ShoppingCart.objects.filter(
                user=data.get('user'),
                recipe=data.get('recipe'),
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок.'
            )
        return data

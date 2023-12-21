from django.db import transaction
from django.shortcuts import get_object_or_404
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
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        queryset=Ingredient.objects.all(),
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True,
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True,
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


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
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

    def get_ingredients(self, obj):
        queryset = RecipeIngredients.objects.filter(recipe=obj)
        return RecipeIngredientsSerializer(
            queryset,
            many=True
        ).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(
            user=user.id,
            recipe=obj.id,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(
            user=user.id,
            recipe=obj.id,
        ).exists()


class IngredientCreateSerializer(serializers.ModelSerializer):
    id = IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = IngredientCreateSerializer(many=True)
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
            'cooking_time'
        )

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Нужно добавить в рецепт хотя бы один ингредиент.'
            )
        ingredients_list = []
        for element in value:
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
        return value

    def validate_tags(self, value):
        tags = value
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
        return value

    @transaction.atomic
    def create_ingredients_amounts(self, ingredients, recipe):
        RecipeIngredients.objects.bulk_create(
            [RecipeIngredients(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
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

    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     tags = validated_data.pop('tags')
    #     if not
    #     ingredients = validated_data.pop('ingredients')
    #     instance = super().update(instance, validated_data)
    #     instance.tags.clear()
    #     instance.tags.set(tags)
    #     instance.ingredients.clear()
    #     self.create_ingredients_amounts(
    #         recipe=instance,
    #         ingredients=ingredients,
    #     )
    #     instance.save()
    #     return instance

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(tags)
        else:
            raise serializers.ValidationError(
                'Отсутствуют теги!'
            )
        if ingredients:
            instance.ingredients.clear()
            self.create_ingredients_amounts(
                recipe=instance,
                ingredients=ingredients,
            )
        else:
            raise serializers.ValidationError(
                'Отсутствуют ингредиенты!'
            )
            # instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeListSerializer(
            instance,
            context={'request': request}
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
                user=self.context.get('request').user,
                recipe=data.get('recipe'),
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже в избранном.'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortVersionSerializer(
            instance.recipe,
            context=context,
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe',
        )

    def validate(self, value):
        request = self.context.get('request')
        recipe = value['recipe']
        if ShoppingCart.objects.filter(
                user=request.user,
                recipe=recipe,
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок.'
            )
        return value

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortVersionSerializer(
            instance.recipe,
            context=context,
        ).data

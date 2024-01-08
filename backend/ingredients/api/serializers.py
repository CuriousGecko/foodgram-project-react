from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.validators import UniqueTogetherValidator

from ingredients.models import Ingredient
from recipes.models import RecipeIngredients


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

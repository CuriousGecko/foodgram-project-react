from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from favorite.models import Favorite
from recipes.api.serializers import RecipeShortSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в избранном.',
            )
        ]

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
        ).data

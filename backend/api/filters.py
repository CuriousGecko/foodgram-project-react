from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
            'ingredients',
        )

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                favorite_recipe__user=self.request.user,
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                buyers__user=self.request.user,
            )
        return queryset


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='startswith',
        method='filter_name',
    )

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )

    def filter_name(self, queryset, name, value):
        return queryset.annotate(
            lower_name=Lower(name)
        ).filter(
            lower_name__startswith=value.lower()
        )

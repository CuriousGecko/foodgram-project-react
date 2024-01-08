from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
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
                favorite_recipes__user=self.request.user,
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                buyers__user=self.request.user,
            )
        return queryset


# Если убрать фильтерсет (реализовать через filterset_fields),
# то как прикрутить 'startswith'. В документации не смог найти.
class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='startswith',
    )

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )

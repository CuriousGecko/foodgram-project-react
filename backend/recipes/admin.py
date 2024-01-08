from django.contrib import admin
from django.contrib.admin import display

from ingredients.admin import IngredientInline
from recipes.models import Recipe, RecipeIngredients


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'author',
        'added_in_favorites',
    )
    readonly_fields = (
        'added_in_favorites',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    inlines = (IngredientInline,)

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorite_recipes.count()

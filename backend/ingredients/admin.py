from django.contrib import admin

from ingredients.models import Ingredient
from recipes.models import RecipeIngredients


class IngredientInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1
    autocomplete_fields = (
        'ingredient',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )

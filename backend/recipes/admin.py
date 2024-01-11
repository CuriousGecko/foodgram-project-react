from django.contrib import admin
from django.contrib.admin import display

from recipes.forms import RecipeIngredientsInlineFormSet
from recipes.models import Recipe, RecipeIngredients


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    formset = RecipeIngredientsInlineFormSet
    extra = 1
    autocomplete_fields = ('ingredient',)


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
    inlines = (RecipeIngredientsInline,)
    filter_horizontal = ('tags',)

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorite_recipes.count()

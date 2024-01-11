from django import forms
from django.core.exceptions import ValidationError


class RecipeIngredientsInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_ingredients = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                ingredient = form.cleaned_data.get('ingredient')
                if ingredient:
                    total_ingredients += 1

        if total_ingredients == 0:
            raise ValidationError(
                'В рецепте должен быть хотя бы один ингредиент.'
            )

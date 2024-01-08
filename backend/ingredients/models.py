from django.db import models

from foodgram_backend.constants import (MAX_LENGHT_INGREDIENT_NAME,
                                        MAX_LENGHT_MEASUREMENT_UNIT)


class Ingredient(models.Model):
    """ Определение модели ингредиента."""

    name = models.CharField(
        'Название',
        unique=True,
        max_length=MAX_LENGHT_INGREDIENT_NAME,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_LENGHT_MEASUREMENT_UNIT,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} измеряется в {self.measurement_unit}.'

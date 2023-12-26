from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from foodgram_backend.constants import (MAX_LENGHT_HEX,
                                        MAX_LENGHT_INGREDIENT_NAME,
                                        MAX_LENGHT_MEASUREMENT_UNIT,
                                        MAX_LENGHT_RECIPE_NAME,
                                        MAX_LENGHT_SLUG, MAX_LENGHT_TAG_NAME,
                                        MIN_AMOUNT, MIN_COOCKING_TIME)

User = get_user_model()


class Tag(models.Model):
    """Определение модели тега."""

    name = models.CharField(
        'Название',
        unique=True,
        max_length=MAX_LENGHT_TAG_NAME,
    )
    color = models.CharField(
        'Цветовой HEX-код',
        unique=True,
        max_length=MAX_LENGHT_HEX,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Некорректный HEX-код.',
            )
        ]
    )
    slug = models.SlugField(
        'Cлаг',
        unique=True,
        max_length=MAX_LENGHT_SLUG,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


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


class Recipe(models.Model):
    """Определение модели рецепта."""

    name = models.CharField(
        'Название',
        max_length=MAX_LENGHT_RECIPE_NAME,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                MIN_COOCKING_TIME,
                message=f'Минимальное значение {MIN_COOCKING_TIME}.',
            )
        ]
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Модель-посредник ингредиентов и рецепта."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=f'Минимальное количество {MIN_AMOUNT}.',
            ),
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class Favorite(models.Model):
    """Определение модели избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_subscribers',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Рецепт',
    )
    when_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_user_in_favorite',
            )
        ]


class ShoppingCart(models.Model):
    """Определение модели корзины покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='buyers',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в корзину покупок.'

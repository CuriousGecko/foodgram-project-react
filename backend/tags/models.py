from django.core.validators import RegexValidator
from django.db import models

from foodgram_backend.constants import (MAX_LENGHT_HEX, MAX_LENGHT_SLUG,
                                        MAX_LENGHT_TAG_NAME)


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

from django.apps import AppConfig


class FavoriteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'favorite'
    verbose_name = 'Избранное'
    verbose_name_plural = 'Избранное'

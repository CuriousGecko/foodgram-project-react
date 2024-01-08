from django.apps import AppConfig


class ShoppingcartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shoppingcart'
    verbose_name = 'Корзина покупок'
    verbose_name_plural = 'Корзины покупок'

from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )

from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = (
        'author__username',
        'author__email',
        'user__username',
        'user__email',
    )
    list_filter = (
        'author__username',
        'user__username',
    )
    empty_value_display = '-пусто-'

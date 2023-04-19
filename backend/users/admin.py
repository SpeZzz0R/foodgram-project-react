from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Модель пользователя в админке"""

    list_display = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['username', 'email']
    empty_value_display = 'пусто'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Модель подписок пользователя в админке"""

    list_display = [
        'id',
        'user',
        'author'
    ]
    search_fields = ['user', 'author']

from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, IngredientsInRecipe,
                     ShoppingCart, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель рецепта блюда в админке"""

    list_display = [
        'id',
        'name',
        'author',
        'text',
        'cooking_time',
        'total_favorites',
        'pub_date'
    ]
    search_fields = ['name', 'author', 'text', 'cooking_time']
    readonly_fields = ['total_favorites']
    list_filter = ['name', 'author', 'pub_date', 'tags']
    empty_value_display = 'пусто'


    @admin.display(description='Всего в избранном')
    def total_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Модель тега в админке"""

    list_display = [
        'id',
        'name',
        'color',
        'slug'
    ]
    search_fields = ['name', 'color', 'slug']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель ингредиентов в админке"""

    list_display = [
        'id',
        'name',
        'measurement_unit'
    ]
    search_fields = ['name', 'measurement_unit']
    list_filter = ['name', 'measurement_unit']


@admin.register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    """Модель ингредиентов для определенного блюда в админке"""

    list_display = [
        'id',
        'recipe',
        'ingredient',
        'amount'
    ]
    search_fields = ['recipe', 'ingredient']
    list_filter = ['recipe', 'ingredient']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Модель любимых рецептов пользователя в админке"""

    list_display = [
        'id',
        'user',
        'recipe'
    ]
    search_fields = ['user', 'recipe']
    list_filter = ['user', 'recipe']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Модель покупок в админке"""

    list_display = [
        'id',
        'user',
        'recipe'
    ]
    search_fields = ['user', 'recipe']
    list_filter = ['user', 'recipe']

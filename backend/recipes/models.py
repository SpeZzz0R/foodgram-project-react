from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(
        verbose_name='Тег',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True)
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['slug']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов"""

    name = models.CharField(
        verbose_name='Наименование ингредиента',
        max_length=200,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""

    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes'
        )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст приготовления рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='IngredientsInRecipe'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления, мин',
        validators=[
            MinValueValidator(
                1,
                message='Минимальное значение: 1 (одна) минута!'
            ),
            MaxValueValidator(
                1440,
                message='Вы уверены, что приготовление блюда занимает '
                        'более одного дня?!'
                )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_author_name'
            )
        ]

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    """Модель ингредиента для определенного блюда"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredientsinrecipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredientsinrecipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Amount',
        validators=[
            MinValueValidator(
                1,
                message='Минимальное количество: 1 (один) ингредиент!'
            ),
            MaxValueValidator(
                100000,
                message='Вы уверены, что для приготовления блюда необходимо '
                        'такое количество ингредиента?!'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ingredient of a recipe'
        verbose_name_plural = 'Ingredients of recipes'
        ordering = ['ingredient']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe} needs {self.amount} of {self.ingredient}'


class Favorite(models.Model):
    """Модель любимых рецептов пользователя"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Название рецепта',
        related_name='favorites',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        ordering = ['recipe']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} added {self.recipe} to favorites'


class ShoppingCart(models.Model):
    """Модель покупок"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='shopping',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Название рецепта',
        related_name='shopping',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'
        ordering = ['recipe']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping'
            )
        ]

    def __str__(self):
        return f'{self.user} added {self.recipe} to shopping cart'

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель данных пользователя"""

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Эл. почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписок пользователя"""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['author']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
        ]

    def __str__(self):
        return f'{self.user} is following to {self.author}'

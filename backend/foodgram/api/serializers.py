from django.db import transaction
from djoser.serializers import (CurrentPasswordSerializer, PasswordSerializer,
                                UserCreateSerializer, UserSerializer)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, Subscription
from recipes.models import Ingredient, Recipe, IngredientsInRecipe, Tag


MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 1440


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации новых пользователей"""

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        ]


class CustomUserSerializer(UserSerializer):
    """Сериализатор для ототбражения информации о пользователях"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.following.filter(user=request.user).exists()


class CustomSetPasswordRetypeSerializer(PasswordSerializer,
                                        CurrentPasswordSerializer):
    """Сериализатор для изменения пароль пользователя"""

    pass


class SubscriptionSerializer(CustomUserSerializer):
    """Сериализатор для подписки на других авторов"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        ]

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        subscription = Subscription.objects.filter(author=author,
                                                   user=user).exists()

        if not subscription:
            raise ValidationError(
                detail='Вы пытаетесь удалить несуществующую подписку',
                code=status.HTTP_400_BAD_REQUEST
            )
        subscription.delete()
        if subscription:
            raise ValidationError(
                detail='Вы уже подписаны на данного пользователя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Нельзя подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].GET.get('recipes_limit')
        if recipes_limit:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        else:
            recipes = obj.recipes.all()
        return RecipeSubscriptionSerializer(recipes,
                                            many=True, read_only=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов определенного рецепта"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsInRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class IngredientsDuringRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов в процессе создания рецепта"""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientsInRecipe
        fields = ['id', 'amount']

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return IngredientsInRecipeSerializer(instance, context=context).data


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов"""

    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsDuringRecipeSerializer(
        many=True, source='ingredientsinrecipe')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.is_favorited(request.user)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.is_in_shopping_cart(request.user)


class RecipeCreateSerializer(RecipeReadSerializer):
    """Сериализатор для создания и обновления рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    ingredients = IngredientsDuringRecipeSerializer(
        source='ingredientsinrecipe', many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time'
        ]

    def validate_tags(self, attrs):
        if len(attrs['tags']) > len(set(attrs['tags'])):
            raise serializers.ValidationError(
                'Нельзя добавить повторяющийся тег несколько раз'
            )
        return attrs

    def validate_ingredients(self, attrs):
        ingredients = [
            item['ingredient'] for item in attrs['ingredientsinrecipe']]
        if len(ingredients) > len(set(ingredients)):
            raise serializers.ValidationError(
                'Нельзя добавить повторяющийся ингредиент несколько раз'
            )
        return attrs

    def validate_cooking_time(self, cooking_time):
        if int(cooking_time) < MIN_COOKING_TIME:
            raise serializers.ValidationError(
                'Время приготовления не можеть занимать '
                'меньше 1 (одной) минуты!')

        if int(cooking_time) > MAX_COOKING_TIME:
            raise serializers.ValidationError(
                'Время приготовления не можеть занимать '
                'больше 1 (одного) дня!')

        return cooking_time

    @transaction.atomic
    def set_recipe_ingredients(self, recipe, ingredients):
        recipe_ingredients = [
            IngredientsInRecipeSerializer(
                recipe=recipe,
                ingredient=current_ingredient['ingredient'],
                amount=current_ingredient['amount']
            )
            for current_ingredient in ingredients
        ]
        IngredientsInRecipeSerializer.objects.bulk_create(recipe_ingredients)

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientsinrecipe')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.set_recipe_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientsinrecipe')
        instance.ingredients.clear()
        instance.tags.clear()
        super().update(instance, validated_data)
        instance.tags.set(tags)
        self.set_recipe_ingredients(instance, ingredients)
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор отображения рецептов на странице подписки"""

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']

from djoser.serializers import (CurrentPasswordSerializer, PasswordSerializer,
                                UserCreateSerializer, UserSerializer)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import status
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from users.models import User, Subscription
from recipes.models import (Ingredient, Recipe, IngredientsInRecipe, Tag,
                            Favorite, ShoppingCart)


MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 1440


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена"""
    email = serializers.EmailField(max_length=254)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        email = list(obj.items())[0][1]
        user = User.objects.get(
            email=email
        )
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    def validate(self, data):
        email = data['email']
        password = data['password']
        try:
            user = User.objects.get(email=email)
        except Exception:
            raise exceptions.AuthenticationFailed('Введенные данные не верные')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Введенные данные не верные')
        return data

    class Meta:
        model = User
        fields = ('email', 'password', 'token')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации новых пользователей"""

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        ]


class CustomUserSerializer(UserSerializer):
    """Сериализатор для отображения информации о пользователях"""

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
    """Сериализатор для изменения пароля пользователя"""

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
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        existing = Favorite.objects.filter(
            user=user.id,
            recipe=obj
        ).exists()
        return existing

    def get_is_in_shopping_cart(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        existing = ShoppingCart.objects.filter(
            user=user.id,
            recipe=obj
        ).exists()
        return existing


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

    def validate_cooking_time(self, cooking_time):
        if int(cooking_time) < MIN_COOKING_TIME:
            raise serializers.ValidationError(
                'Время приготовления не может занимать '
                'меньше 1 (одной) минуты!')

        if int(cooking_time) > MAX_COOKING_TIME:
            raise serializers.ValidationError(
                'Время приготовления не может занимать '
                'больше 1 (одного) дня!')

        return cooking_time

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientsInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient.get('ingredient'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredientsinrecipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        if 'ingredientsinrecipe' in validated_data:
            ingredients = validated_data.pop('ingredientsinrecipe')
            if 'ingredientsinrecipe':
                recipe.ingredients.clear()
            RecipeCreateSerializer.create_ingredients(
                self, ingredients, recipe
            )
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок"""
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_id(self, obj):
        return obj.recipe.id

    def get_name(self, obj):
        return obj.recipe.name

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.recipe.image)

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time

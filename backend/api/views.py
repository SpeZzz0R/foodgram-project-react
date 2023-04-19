from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as rf_filters

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomSetPasswordRetypeSerializer,
                          CustomUserCreateSerializer, CustomUserSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipeSubscriptionSerializer, RecipeReadSerializer,
                          SubscriptionSerializer, TagSerializer)
from users.models import Subscription, User
from recipes.models import (Favorite, Ingredient, Recipe, IngredientsInRecipe,
                            ShoppingCart, Tag)


class UserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для регистрации и отображения пользователей"""

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={
                'request': request,
                'format': self.format_kwarg,
                'view': self
            }
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        subscription = Subscription.objects.filter(
            user=request.user, author=author)
        if request.method == 'DELETE' and not subscription:
            return Response(
                {'errors': 'Вы пытаетесь удалить несуществующую подписку'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if subscription:
            return Response(
                {'errors': 'Вы уже подписаны на данного пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if author == request.user:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.create(user=request.user, author=author)
        serializer = SubscriptionSerializer(
            author,
            context={
                'request': request,
                'format': self.format_kwarg,
                'view': self
            }
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SelfUserView(views.APIView):
    """Вьюкласс текущего пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(
            request.user,
            context={
                'request': request,
                'format': self.format_kwarg,
                'view': self
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetPasswordRetypeView(views.APIView):
    """Вьюкласс изменения пароля пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CustomSetPasswordRetypeSerializer(
            data=request.data,
            context={
                'request': request,
                'format': self.format_kwarg,
                'view': self
            }
        )
        if serializer.is_valid():
            self.request.user.set_password(serializer.data['new_password'])
            self.request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = [rf_filters.DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов"""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [rf_filters.DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def create_delete_or_scold(self, model, recipe, request):
        instance = model.objects.filter(recipe=recipe, user=request.user)
        name = model.__name__
        if request.method == 'DELETE' and not instance:
            return Response(
                {'errors': f'В Вашем списке не было рецепта: {name}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if instance:
            return Response(
                {'errors': f'{name} уже добавлен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeSubscriptionSerializer(
            recipe,
            context={
                'request': request,
                'format': self.format_kwarg,
                'view': self
            }
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return self.create_delete_or_scold(Favorite, recipe, request)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return self.create_delete_or_scold(ShoppingCart, recipe, request)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        header_font_size = 20
        body_font_size = 15
        header_left_margin = 100
        body_left_margin = 80
        header_height = 770
        body_first_line_height = 740
        line_spacing = 20
        bottom_margin = 100
        bullet_point_symbol = u'\u2022'

        recipes_ingredients = IngredientsInRecipe.objects.filter(
            recipe__shopping__user=request.user).order_by('ingredient')
        cart = recipes_ingredients.values(
            'ingredient__name', 'ingredient__measurement_unit',
        ).annotate(total=Sum('amount'))

        shopping_list = []
        for ingredient in cart:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            total = ingredient['total']
            line = bullet_point_symbol + f' {name} - {total} {unit}'
            recipes = recipes_ingredients.filter(ingredient__name=name)
            recipes_names = [
                (item.recipe.name, item.amount) for item in recipes]
            shopping_list.append((line, recipes_names))

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping.pdf"'
        paper_sheet = canvas.Canvas(response, pagesize=A4)
        registerFont(TTFont('FreeSans', 'FreeSans.ttf'))

        paper_sheet.setFont('FreeSans', header_font_size)
        paper_sheet.drawString(
            header_left_margin, header_height, 'Список покупок')

        paper_sheet.setFont('FreeSans', body_font_size)
        y_coordinate = body_first_line_height
        for ingredient, recipes_names in shopping_list:
            paper_sheet.drawString(body_left_margin, y_coordinate, ingredient)
            y_coordinate -= line_spacing

            for recipe_name in recipes_names:
                if y_coordinate <= bottom_margin:
                    paper_sheet.showPage()
                    y_coordinate = body_first_line_height
                    paper_sheet.setFont('FreeSans', body_font_size)
                recipe_line = f'  {recipe_name[0]} ({recipe_name[1]})'
                paper_sheet.drawString(
                    body_left_margin, y_coordinate, recipe_line)
                y_coordinate -= line_spacing

            if y_coordinate <= bottom_margin:
                paper_sheet.showPage()
                y_coordinate = body_first_line_height
                paper_sheet.setFont('FreeSans', body_font_size)

        paper_sheet.showPage()
        paper_sheet.save()
        return response

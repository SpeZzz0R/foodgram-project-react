from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, SelfUserView,
                    SetPasswordRetypeView, TagViewSet, UserViewSet,
                    get_token)

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('users/me/', SelfUserView.as_view()),
    path('users/set_password/', SetPasswordRetypeView.as_view()),
    path('', include(router.urls)),
    path('auth/token/login/', get_token),
    path('auth/', include('djoser.urls.authtoken')),
    # path(r'auth/token/login/', TokenCreateView.as_view(), name='login'),
    # path(r'auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
]

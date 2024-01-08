from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients.api.views import IngredientViewSet
from recipes.api.views import RecipeViewSet
from tags.api.views import TagViewSet
from users.api.views import CustomUserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'auth/',
        include('djoser.urls.authtoken'),
    ),
    path(
        '',
        include(router.urls),
    ),
]

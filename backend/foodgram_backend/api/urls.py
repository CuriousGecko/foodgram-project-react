from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients.api.views import IngredientViewSet
from recipes.api.views import RecipeViewSet
from subscriptions.api.views import APISubscribe, APISubscriptions
from tags.api.views import TagViewSet
from users.api.views import UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'users/<int:id>/subscribe/',
        APISubscribe.as_view(),
        name='subscribe',
    ),
    path(
        'users/subscriptions/',
        APISubscriptions.as_view(),
        name='subscriptions',
    ),
    path(
        'auth/',
        include('djoser.urls.authtoken'),
    ),
    path(
        '',
        include(router.urls),
    ),
]

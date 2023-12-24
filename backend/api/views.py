from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeReadSerializer, RecipeSerializer,
                             ShoppingCartSerializer, TagSerializer)
from foodgram_backend.constants import DOWNLOAD_FILENAME
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                            ShoppingCart, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатывает запросы, связанные с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатывает запросы, связанные с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы, связанные с рецептами, избранным и корзиной."""

    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly | IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def favorite(self, request, pk):
        return self.add_obj(request, pk, FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_obj(request, pk, Favorite)

    @action(
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def shopping_cart(self, request, pk):
        return self.add_obj(request, pk, ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_obj(request, pk, ShoppingCart)

    def add_obj(self, request, pk, serializer):
        serializer = serializer(
            data={
                'user': self.request.user.id,
                'recipe': pk,
            }
        )
        serializer.is_valid(
            raise_exception=True,
        )
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete_obj(self, request, pk, model):
        error_messages = {
            Favorite: 'Нельзя удалить рецепт из избранного, '
                      'который не был туда добавлен.',
            ShoppingCart: 'Нельзя удалить рецепт из корзины, '
                          'который не был туда добавлен.',
        }
        recipe_in = model.objects.filter(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, pk=pk),
        )
        if not recipe_in.exists():
            return Response(
                error_messages.get(model),
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe_in.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(
            user=user,
        )
        if not shopping_cart.exists():
            return Response(
                'Ваша корзина покупок пуста.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        ingredients = RecipeIngredients.objects.filter(
            recipe__buyers__user=user,
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(
            amount=Sum('amount'),
        )
        shopping_list = [
            f'{index + 1}. {ingredient["ingredient__name"]} '
            f'- {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for index, ingredient in enumerate(ingredients)
        ]
        shopping_list_text = 'Нужно купить:\n', '\n'.join(shopping_list)
        response = HttpResponse(
            shopping_list_text,
            content_type='text/plain',
        )
        response['Content-Disposition'] = (
            f'attachment; filename={DOWNLOAD_FILENAME}'
        )
        return response

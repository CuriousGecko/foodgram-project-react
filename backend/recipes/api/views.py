from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favorite.api.serializers import FavoriteSerializer
from favorite.models import Favorite
from foodgram_backend.api.filters import RecipeFilter
from foodgram_backend.api.pagination import Pagination
from foodgram_backend.api.permissions import (IsAdminOrReadOnly,
                                              IsOwnerOrReadOnly)
from recipes.api.serializers import RecipeWriteSerializer
from recipes.api.utils import download_pdf
from recipes.models import Recipe, RecipeIngredients
from shoppingcart.api.serializers import ShoppingCartSerializer
from shoppingcart.models import ShoppingCart


class RecipeViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы, связанные с рецептами, избранным и корзиной."""

    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly | IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = Pagination
    serializer_class = RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        serializer_class=FavoriteSerializer,
        detail=True,
    )
    def favorite(self, request, pk):
        return self.add_obj(request, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_obj(request, pk, Favorite)

    @action(
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        serializer_class=ShoppingCartSerializer,
        detail=True,
    )
    def shopping_cart(self, request, pk):
        return self.add_obj(request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_obj(request, pk, ShoppingCart)

    def add_obj(self, request, pk):
        serializer = self.get_serializer_class()
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
        shopping_list = self.shopping_list_create(ingredients)
        return download_pdf(shopping_list)

    def shopping_list_create(self, ingredients):
        shopping_list = [
            f'{index + 1}. {ingredient["ingredient__name"]} '
            f'- {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for index, ingredient in enumerate(ingredients)
        ]
        return shopping_list

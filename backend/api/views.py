from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeSerializer, ShoppingCartSerializer,
                             TagSerializer)
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly | IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def favorite(self, request, pk):
        serializer = FavoriteSerializer(
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

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        recipe_in_favorite = Favorite.objects.filter(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, pk=pk),
        )
        if not recipe_in_favorite.exists():
            return Response(
                'Нельзя удалить рецепт из избранного, '
                'который не был туда добавлен.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe_in_favorite.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def shopping_cart(self, request, pk):
        serializer = ShoppingCartSerializer(
            data={
                'user': self.request.user.id,
                'recipe': pk,
            },
        )
        serializer.is_valid(
            raise_exception=True,
        )
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        recipe_in_shopping_cart = ShoppingCart.objects.filter(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, pk=pk),
        )
        if not recipe_in_shopping_cart.exists():
            return Response(
                'Нельзя удалить рецепт из корзины, '
                'который не был туда добавлен.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe_in_shopping_cart.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

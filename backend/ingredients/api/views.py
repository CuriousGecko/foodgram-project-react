from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from foodgram_backend.api.filters import IngredientFilter
from ingredients.api.serializers import IngredientSerializer
from ingredients.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатывает запросы, связанные с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None

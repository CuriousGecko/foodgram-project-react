from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from tags.api.serializers import TagSerializer
from tags.models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатывает запросы, связанные с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from foodgram_backend.api.pagination import Pagination


class UserViewSet(DjoserUserViewSet):
    """Обрабатывает запросы, связанные с пользователями."""

    pagination_class = Pagination

    @action(
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def me(self, request):
        return super().me(request)

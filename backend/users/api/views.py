from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import IsAuthenticated

from foodgram_backend.api.pagination import Pagination


class UserViewSet(DjoserUserViewSet):
    """Обрабатывает запросы, связанные с пользователями."""

    pagination_class = Pagination

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)
        return super().get_permissions()

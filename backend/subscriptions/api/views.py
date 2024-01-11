from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from foodgram_backend.api.pagination import Pagination
from subscriptions.api.serializers import (SubscriptionCreateSerializer,
                                           SubscriptionListSerializer)
from subscriptions.models import Subscription

User = get_user_model()


# Это конечно не столь элегантно, но почему бы и да.
# По мне разумный компромисс для идеи разделения приложений\вьюх.
# Да и будет хоть пример с APIView для разнообразия.
# А экшоны и в других местах есть.
class APISubscribe(APIView):
    """Создаст или удалит подписку на пользователя."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        user = request.user
        author = get_object_or_404(
            User,
            id=id,
        )
        serializer = SubscriptionCreateSerializer(
            data={'user': user.id, 'author': author.id},
            context={'request': request, 'author': author},
        )
        serializer.is_valid(
            raise_exception=True,
        )
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, id):
        author = get_object_or_404(
            User,
            id=id,
        )
        subscription = Subscription.objects.filter(
            user=request.user,
            author=author,
        )
        if not subscription.exists():
            return Response(
                'Нельзя удалить несуществующую подписку на пользователя.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class APISubscriptions(APIView):
    """Вернет список подписок пользователя."""

    pagination_class = Pagination
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        subscriptions = User.objects.filter(
            following__user=request.user,
        )
        paginator = self.pagination_class()
        subscriptions = paginator.paginate_queryset(subscriptions, request)
        serializer = SubscriptionListSerializer(
            subscriptions,
            many=True,
            context={'request': request},
        )
        return paginator.get_paginated_response(serializer.data)

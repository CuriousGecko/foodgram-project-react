from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from foodgram_backend.api.pagination import Pagination
from subscriptions.api.serializers import (SubscriptionCreateSerializer,
                                           SubscriptionListSerializer)
from subscriptions.models import Subscription

User = get_user_model()


class SubscribeAPI(APIView):
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


class SubscriptionListViewSet(ListModelMixin, GenericViewSet):
    """Вернет список подписок пользователя."""

    serializer_class = SubscriptionListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = Pagination

    def get_queryset(self):
        return User.objects.filter(
            following__user=self.request.user,
        )

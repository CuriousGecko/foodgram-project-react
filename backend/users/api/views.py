from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram_backend.api.pagination import CustomPagination
from users.models import Subscription
from users.api.serializers import (SubscriptionCreateSerializer,
                                   SubscriptionListSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Обрабатывает запросы, связанные с пользователями и подписками."""

    pagination_class = CustomPagination

    @action(
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def subscribe(self, request, id):
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

    @subscribe.mapping.delete
    def delete_subscription(self, request, id):
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

    @action(
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            following__user=request.user,
        )
        pages = self.paginate_queryset(subscriptions)
        serializer = SubscriptionListSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    # По умолчанию он набор методов может. В ТЗ лишь GET.
    # Так-то вроде не критично, но будут светиться ненужные методы в доступных.
    @action(
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def me(self, request):
        self.get_object = self.get_instance
        return self.retrieve(request)

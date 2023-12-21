from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPagination
from users.serializers import UserSubscribesSerializer

from .models import Subscription

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination

    @action(
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(
            User,
            id=self.kwargs.get('id'),
        )
        serializer = UserSubscribesSerializer(
            author,
            data={},
            context={'request': request},
        )
        serializer.is_valid(
            raise_exception=True,
        )
        Subscription.objects.create(
            user=user,
            author=author,
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @subscribe.mapping.delete
    def delete_subscription(self, request, **kwargs):
        author = get_object_or_404(
            User,
            id=self.kwargs.get('id'),
        )
        subscription = Subscription.objects.filter(
            user=request.user,
            author=author,
        )
        if not subscription:
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
        serializer = UserSubscribesSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def me(self, request):
        self.get_object = self.get_instance
        return self.retrieve(request)

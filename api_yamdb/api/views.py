from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import (
    IsAuthenticated, AllowAny
)
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.decorators import action

from reviews.models import User
from .serializers import SingUpSerializer, TokenSerializer, UserSerializer
from .permissions import (
    IsAdminOrSuperUserDjango,
    IsSuperUserOrAdminOrModeratorOrAuthorOrReadOnly
)


class SingUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Создание обьектов класса User и отправка кода подтвердения."""
    serializer_class = SingUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SingUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**request.data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email='zbls@pzdc.ru',
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Создание токена для пользователя."""
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            message = {'token': str(AccessToken.for_user(user))}
            return Response(message, status=status.HTTP_200_OK)
        message = {'confirmation_code': 'Код подтверждения неверен'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для юзеров."""
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSuperUserDjango,)
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='detail_user',
    )
    def detail_user(self, request, username):
        """Работа с конкретным пользователем."""
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_data_about_me(self, request):
        """Получение и редактирование информации о себе."""
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

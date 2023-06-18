from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Categories, Genres, Review, Titles, User

from .permissions import (
    IsAdminModeratorOwnerOrReadOnly,
    IsAdminOrSuperUserDjango
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReadOnlyTitleSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer
)


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Создание обьектов класса User и отправка кода подтвердения."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        if (
            not serializer.is_valid()
            and not User.objects.filter(**serializer.data)
        ):
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user, x = User.objects.get_or_create(**serializer.data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'ваш "confirmation_code": {confirmation_code}',
            from_email='zbls@pzdc.ru',
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Создание токена для пользователя."""
    queryset = User.objects.all()
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
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для юзеров."""
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSuperUserDjango,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user'
    )
    def get_user_by_username(self, request, username):
        """Обеспечивает получание данных пользователя по его username и
        управление ими."""
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateDestroyViewSet):
    """Категорий сет, фильтрация вынесена в CreateDestroyViewSet."""
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyViewSet):
    """Жанр сет, фильтрация вынесена в CreateDestroyViewSet."""
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Тайтлвью сет фильтрация, создание и обновление."""
    # Добавил anotate для подсчета рейтинга.
    queryset = Titles.objects.all().annotate(
        Avg("reviews__score")
    )
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('name', 'category__slug', 'genre__slug', 'year',)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет работы с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly, )

    def get_title(self):
        """Метод получения произведения, для которого пишется отзыв."""
        return get_object_or_404(Titles, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Метод получения списка отзывов."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Метод создания отзыва, с текущим пользователем в поел author."""
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly, )

    def get_review(self):
        """Метод получения отзыва, к которому пишется комментарий."""
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Метод получения списка комментариев."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)

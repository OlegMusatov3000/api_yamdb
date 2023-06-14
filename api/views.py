from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Title

from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет работы с отзывами."""
    serializer_class = ReviewSerializer
    # Пока не настроены точные пермишены, оставлю этот пермишн.
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_title(self):
        """Метод получения произведения, для которого пишется отзыв."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Метод получения списка отзывов."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Метод создания отзыва, с текущим пользователем в поел author."""
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

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

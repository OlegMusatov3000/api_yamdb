from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from api.serializers import (TitleSerializer,
                             CategorySerializer,
                             GenreSerializer)

from reviews.models import Titles, Categories, Genres


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class CategoryViewSet(CreateDestroyViewSet):
    """Категорий сет, фильтрация вынесена в CreateDestroyViewSet."""
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyViewSet):
    """Жанр сет, фильтрация вынесена в CreateDestroyViewSet."""
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Тайтлвью сет фильтрация, создание и обновление."""
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('name', 'category__slug', 'genre__slug', 'year',)

    def perform_create(self, serializer):
        return serializer.save(
            category=get_object_or_404(self.request.data.get('category')),
            genre=get_object_or_404(self.request.data.get('genre')))

    def perform_update(self, serializer):
        return serializer.save(
            category=get_object_or_404(self.request.data.get('category')),
            genre=get_object_or_404(self.request.data.get('genre')))

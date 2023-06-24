from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.filters import SearchFilter

"""Вынес миксины в отдельный файл и добавил для тайтлов."""


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    filter_backends = (SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    pagination_class = PageNumberPagination

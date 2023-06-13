from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (TitleViewSet,
                       CategoryViewSet,
                       GenreViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('', include(router.urls)),
]

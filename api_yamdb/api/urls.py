from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (
  SignUpViewSet,
  TokenViewSet,
  UserViewSet,
  TitleViewSet,
  CategoryViewSet,
  GenreViewSet


app_name = 'api'

router = DefaultRouter()

router.register(
    'titles', TitleViewSet, basename='titles')
router.register(
    'categories', CategoryViewSet, basename='categories')
router.register(
    'genres', GenreViewSet, basename='genres')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignUpViewSet.as_view(
        {'post': 'create'}), name='singup'),
    path('auth/token/', TokenViewSet.as_view(
        {'post': 'create'}), name='token'),
    path('', include(router.urls)),
]

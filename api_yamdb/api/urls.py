from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (
    SignUpViewSet,
    TokenViewSet,
    UserViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    CommentViewSet,
    ReviewViewSet,
)


app_name = 'api'

router = DefaultRouter()

router.register(
    'titles', TitleViewSet, basename='titles')
router.register(
    'categories', CategoryViewSet, basename='categories')
router.register(
    'genres', GenreViewSet, basename='genres')
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', SignUpViewSet.as_view(
        {'post': 'create'}), name='singup'),
    path('token/', TokenViewSet.as_view(
        {'post': 'create'}), name='token'),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls)),
]

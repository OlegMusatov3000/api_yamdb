from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SingUpViewSet, TokenViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/singup/', SingUpViewSet.as_view(
        {'post': 'create'}), name='singup'),
    path('auth/token/', TokenViewSet.as_view(
        {'post': 'create'}), name='token'),
    path('', include(router.urls))
]

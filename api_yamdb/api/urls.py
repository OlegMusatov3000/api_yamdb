from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import SingUpViewSet

app_name = 'api'

#router = SimpleRouter()
#router.register(r'auth/singup', SingUpViewSet)

urlpatterns = [
    path('auth/singup/', SingUpViewSet.as_view(
        {'post': 'create'})),
    #path('auth/token', TokenViewSet),
]

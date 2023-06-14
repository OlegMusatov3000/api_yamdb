from django.core.mail import send_mail
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
)
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.tokens import default_token_generator
from reviews.models import User
from .serializers import SingUpSerializer
from .permissions import IsAuthorOrReadOnly



class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class SingUpViewSet(CreateViewSet):
    serializer_class = SingUpSerializer
    permission_classes = (AllowAny,)
    send_mail(
        'Тема письма',
        'ваш код = default_token_generator.make_token())',
        'testtestovic351@gmail.com',  # Это поле "От кого"
        ['testtestovic351@gmail.com'],  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False, # Сообщать об ошибках («молчать ли об ошибках?»)
)

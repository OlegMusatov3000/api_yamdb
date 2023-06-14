from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.TextField(
        'Пользовательская роль',
        blank=True,
        choices=(
            ('user', 'пользователь'),
            ('moderator', 'модератор'),
            ('admin', 'администратор')
        ),
    )

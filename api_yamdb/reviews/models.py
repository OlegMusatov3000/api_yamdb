from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models
import datetime as dt


class User(AbstractUser):
    """Класс пользователей."""
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        db_index=True,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Неправильное имя пользователя!'
        )]
    )
    email = models.EmailField(
        'почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True
    )
    role = models.TextField(
        'Пользовательская роль',
        blank=True,
        choices=(
            ('user', 'пользователь'),
            ('moderator', 'модератор'),
            ('admin', 'администратор')
        ),
        default='user'
    )


class Categories(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Модель произведений, с ограничением по году выхода."""
    name = models.CharField(max_length=256)
    year = models.IntegerField(verbose_name='Год выхода',
                               validators=
                               [MaxValueValidator(dt.date.today().year)])
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(Genres,
                                   related_name='titles',
                                   verbose_name='Жанры')
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='Категории',
                                 null=True,
                                 blank=True)

    def __str__(self):
        return self.name

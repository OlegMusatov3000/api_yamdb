from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
)
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
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Модель произведений, с ограничением по году выхода."""
    name = models.CharField(max_length=256)
    year = models.IntegerField(
        verbose_name='Год выхода',
        validators=[MaxValueValidator(dt.date.today().year)]
    )
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


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    score = models.IntegerField(
        verbose_name="Оценка",
        validators=[
            MaxValueValidator(10, 'Значение не может быть выше 10'),
            MinValueValidator(1, 'Значение не может быть меньше 1')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='uniq_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

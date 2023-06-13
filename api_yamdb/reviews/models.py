from django.db import models
from django.core.validators import MaxValueValidator
import datetime as dt


class Categories(models.Model):
    """Модель категорий"""
    name = models.CharField(max_length=256
                            )
    slug = models.SlugField(max_length=50,
                            unique=True
                            )

    def __str__(self):
        return self.name


class Genres(models.Model):
    """Модель жанров"""
    name = models.CharField(max_length=256
                            )
    slug = models.SlugField(max_length=50,
                            unique=True
                            )

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Модель произведений, с ограничением по году выхода"""
    name = models.CharField(max_length=256)
    year = models.IntegerField(verbose_name='Год выхода',
                               validators=
                               [MaxValueValidator(dt.date.today().year)])
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(Genres,
                                   related_name='titles',
                                   verbose_name='Жанры'
                                   )
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='Категории',
                                 null=True,
                                 blank=True
                                 )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name

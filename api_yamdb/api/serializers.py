from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (Titles, Genres, Categories)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        fields = ('name', 'slug',)
        look_up_field = 'slug'
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        fields = ('name', 'slug',)
        look_up_field = 'slug'
        model = Genres


class TitleSerializer(serializers.ModelSerializer):
    """Тайтл сериализатор."""
    category = SlugRelatedField(slug_field='slug',
                                read_only=True)
    genre = SlugRelatedField(slug_field='slug',
                             read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles

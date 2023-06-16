from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
  Titles,
  Genres,
  Categories,
  User,
)


class SignUpSerializer(serializers.ModelSerializer):
    """Создает нового пользователя при регистрации."""

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для объекта класса User при получении токена JWT."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для зарегистрированного Юзера."""

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return username



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

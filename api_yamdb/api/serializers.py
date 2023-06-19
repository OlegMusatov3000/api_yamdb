from rest_framework import serializers

from reviews.models import (
    Title,
    Genre,
    Category,
    User,
    Comment,
    Review,
)


class SignUpSerializer(serializers.ModelSerializer):
    """Создает нового пользователя при регистрации."""

    class Meta:
        fields = ('email', 'username',)
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
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
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
        lookup_fields = ('slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Тайтл сериализатор."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())

    def create(self, validated_data):
        """Создания жанра категории."""
        genre_data = self.context['request'].data.get('genre', [])
        category_data = self.context['request'].data.get('category')
        genres = Genre.objects.filter(slug__in=genre_data)
        category = Category.objects.get(slug=category_data)
        validated_data['category'] = category
        validated_data.pop('genre', None)
        title = Title.objects.create(**validated_data)
        title.genre.set(genres)
        return title

    def update(self, instance, validated_data):
        """Изменения жанров категорий."""
        genre_data = self.context['request'].data.get('genre', [])
        category_data = self.context['request'].data.get('category')
        genres = Genre.objects.filter(slug__in=genre_data)
        category = Category.objects.get(slug=category_data)
        validated_data['category'] = category
        if 'genre' in validated_data:
            validated_data.pop('genre')
        instance = super().update(instance, validated_data)
        instance.genre.set(genres)
        return instance

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerReadOnly(serializers.ModelSerializer):
    """Тайтл сериализатор для рид онли запросов."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    title=self.context['view'].kwargs.get('title_id'),
                    author=self.context['request'].user
            ).exists():
                raise serializers.ValidationError(
                    'Можно добавить только 1 отзыв на произведение!'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text',
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = '__all__'

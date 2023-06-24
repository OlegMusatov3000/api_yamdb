from rest_framework import serializers

from reviews.models import (
    Title,
    Genre,
    Category,
    User,
    Comment,
    Review,
)

BLACK_LIST_USERNAMES = ('me',)


class SignUpSerializer(serializers.ModelSerializer):
    """Создает нового пользователя при регистрации."""

    class Meta:
        fields = ('email', 'username',)
        model = User

    def validate(self, data):
        """Запрещает использовать имена из списка запрещенных username."""
        if data.get('username') in BLACK_LIST_USERNAMES:
            raise serializers.ValidationError(
                'использование такого имени недопустимо'
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
        """Запрещает использовать имена из списка запрещенных username."""
        if username in BLACK_LIST_USERNAMES:
            raise serializers.ValidationError(
                'использование такого имени недопустимо'
            )
        return username


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = ('name', 'slug',)
        model = Category
        queryset = Category.objects.all()


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров."""

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genre
        queryset = Genre.objects.all()


class SlugFieldWithDictRepresent(serializers.SlugRelatedField):
    def to_representation(self, instance):
        return {'name': instance.name, 'slug': instance.slug}


class TitleSerializer(serializers.ModelSerializer):
    """Тайтл сериализатор."""
    category = SlugFieldWithDictRepresent(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = SlugFieldWithDictRepresent(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug')

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
                    title_id=self.context['view'].kwargs.get('title_id', None),
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

from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from reviews.models import User


class SingUpSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username')
        model = User

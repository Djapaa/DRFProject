from rest_framework import serializers
from django.contrib.auth import get_user_model

from ..composition.models import UserCompositionRelation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class BookmarkSerializer(serializers.ModelSerializer):
    composition = serializers.IntegerField(write_only=True)
    class Meta:
        model = UserCompositionRelation
        fields = ('id', 'composition', 'bookmark')

class RatingSerializer(BookmarkSerializer):
    class Meta:
        model = UserCompositionRelation
        fields = ('id', 'composition', 'rating')

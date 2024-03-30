from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..composition.models import UserCompositionRelation, Composition

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class BookmarkEditSerializer(serializers.ModelSerializer):
    composition = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserCompositionRelation
        fields = ('id', 'composition', 'bookmark')


class RatingEditSerializer(BookmarkEditSerializer):
    class Meta:
        model = UserCompositionRelation
        fields = ('id', 'composition', 'rating')


class CompositionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = ('id', 'title', 'english_title', 'slug', 'composition_image')


class ChapterBookmarkSerializer(serializers.ModelSerializer):
    composition = CompositionDetailSerializer()

    class Meta:
        model = UserCompositionRelation
        exclude = ('user',)

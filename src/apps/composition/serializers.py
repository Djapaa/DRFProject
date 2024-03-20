from rest_framework import serializers
from taggit.models import Tag

from .models import CompositionsType, Author, Genre, CompositionsStatus, Composition, CompositionsAgeRating


class CompositionsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompositionsStatus
        fields = '__all__'


class CompositionsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompositionsType
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CompositionsAgeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompositionsAgeRating
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CompositionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    type = CompositionsTypeSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    status = CompositionsStatusSerializer(read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    age_rating = CompositionsAgeRatingSerializer(read_only=True)

    class Meta:
        model = Composition
        fields = ('id', 'slug', 'title', 'english_title',
                  'another_name_title', 'age_rating', 'type', 'genre',
                  'year_of_creations', 'created', 'updated',
                  'description', 'composition_image', 'view',
                  'status', 'author', 'tags')

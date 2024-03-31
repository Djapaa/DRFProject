from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import CompositionsType, Author, Genre, CompositionsStatus, Composition, CompositionsAgeRating, Tag

class PublishersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'username')

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


class CatalogSearchListSerializer(serializers.ModelSerializer):
    """"""
    type = serializers.CharField(source='type.name')
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    # api_detail_url = serializers.HyperlinkedIdentityField(view_name='composition-detail', lookup_field='slug')
    dir = serializers.CharField(source='slug', read_only=True)
    composition_image = serializers.ImageField()


    class Meta:
        model = Composition
        fields = ('id', 'slug', 'title', 'composition_image', 'type', 'avg_rating', 'dir')


class CompositionDetailSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    type = CompositionsTypeSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    status = CompositionsStatusSerializer(read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    publishers = PublishersSerializer(many=True, read_only=True)

    age_rating = CompositionsAgeRatingSerializer(read_only=True)
    count_rating = serializers.IntegerField(read_only=True)
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=1, read_only=True)
    total_in_bookmarks = serializers.IntegerField(read_only=True)


    class Meta:
        model = Composition
        exclude = ('updated', 'created', 'readers')


class CompositionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        exclude = (
            'slug',
            'created',
            'updated',
            'publishers',
            'view',
            'readers',
        )
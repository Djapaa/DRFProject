
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import Chapter, Page

User = get_user_model()


class ChapterListSerializer(serializers.ModelSerializer):
    """ Сериализует главы """
    class Meta:
        model = Chapter
        fields = ('id', 'is_published', 'number', 'name', 'upload_date', 'pub_date')


class PageListSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(min_value=0)
    class Meta:
        model = Page
        fields = ('image_page', 'number')

class PageListCreateSerializer(PageListSerializer):
    number = serializers.IntegerField(min_value=0, read_only=True)



class ChapterDetailSerializer(serializers.ModelSerializer):
    pages = PageListSerializer(many=True)
    upload_date = serializers.DateTimeField(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Chapter
        fields = ('id', 'is_published', 'number', 'name', 'upload_date', 'pub_date', 'pages')


class ChapterUpdateSerializer(serializers.ModelSerializer):
    """ Обновелиние главы и ее страниц"""
    pages = PageListSerializer(many=True, required=False)
    number = serializers.IntegerField(min_value=0, validators=[UniqueValidator(queryset=Chapter.objects.all())])

    class Meta:
        model = Chapter
        fields = ('number', 'name', 'is_published', 'pages')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.number = validated_data.get('number', instance.number)
        pages = validated_data.pop('pages', None)
        if pages:
            for page in pages:
                instance.pages.filter(number=page['number']).update(image_page=page['image_page'])
        instance.save()
        return instance




class ChapterCreateSerializer(serializers.ModelSerializer):
    """ Создание главы и ее страниц"""
    pages = PageListCreateSerializer(many=True)
    number = serializers.IntegerField(min_value=0)

    def validate(self, attrs):
        number = attrs.get('number')
        composition_id = self.context.get('composition_id')
        try:
            Chapter.objects.get(number=number, composition_id=composition_id)
        except Chapter.DoesNotExist:
            return attrs
        raise serializers.ValidationError('Глава под таким номером уже существует')
    class Meta:
        model = Chapter
        fields = ('number', 'name', 'pages')


    def create(self, validated_data):
        pages = validated_data.pop('pages')
        chapter = Chapter.objects.create(**validated_data)
        for number, page in enumerate(pages, 1):
            Page.objects.create(chapter=chapter, number=number, **page)
        return chapter

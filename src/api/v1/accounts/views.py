
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import BookmarkEditSerializer, RatingEditSerializer, ChapterBookmarkSerializer
from ..composition.models import UserCompositionRelation, Composition

User = get_user_model()


class BookmarkEditView(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['bookmark']

    ordering_fields = ['id', ]


    def get_object(self):
        return get_object_or_404(User.objects.only('id'), pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return UserCompositionRelation.objects.filter(user_id=self.get_object().id).select_related(
            'composition'
        ).only(
            'id',
            'composition__id',
            'composition__title',
            'composition__english_title',
            'composition__composition_image',
            'composition__slug',
            'bookmark',
            'rating',
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return BookmarkEditSerializer
        return ChapterBookmarkSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        composition = get_object_or_404(Composition, pk=serializer.validated_data.get('composition'))

        instance, _ = UserCompositionRelation.objects.get_or_create(user=self.request.user,
                                                                    composition=composition)
        instance.bookmark = serializer.validated_data.get('bookmark')
        instance.save()

        return Response(
            {
                'id': instance.id,
                'bookmark': instance.bookmark
            }, status=status.HTTP_200_OK
        )


class RatingEditView(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = RatingEditSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        composition = get_object_or_404(Composition, pk=serializer.validated_data.get('composition'))
        instance, _ = UserCompositionRelation.objects.get_or_create(user=self.request.user,
                                                                    composition=composition)
        instance.rating = serializer.validated_data.get('rating')
        instance.save()

        return Response(
            {
                'rating': instance.rating,
            }, status=status.HTTP_200_OK
        )

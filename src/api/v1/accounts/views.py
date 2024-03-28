from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .serializers import BookmarkSerializer, RatingSerializer
from ..composition.models import UserCompositionRelation


class BookmarkEditView(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = BookmarkSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance, _ = UserCompositionRelation.objects.get_or_create(user=self.request.user,
                                                                    composition_id=serializer.validated_data.get(
                                                                        'composition'))
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
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance, _ = UserCompositionRelation.objects.get_or_create(user=self.request.user,
                                                                    composition_id=serializer.validated_data.get(
                                                                        'composition'))
        instance.rating = serializer.validated_data.get('rating')
        instance.save()

        return Response(
            {
                'rating': instance.rating,
            }, status=status.HTTP_200_OK
        )

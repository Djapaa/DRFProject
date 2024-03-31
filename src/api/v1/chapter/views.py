from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from ..viewsets.permissions import IsOwnerChapter
from .models import Chapter
from .serializers import ChapterListSerializer, ChapterDetailSerializer, ChapterCreateSerializer, \
    ChapterUpdateSerializer
from ..composition.models import Composition


class ChapterListView(ListAPIView):
    """ Вывод всех глав произведения"""
    serializer_class = ChapterListSerializer

    def get_queryset(self):
        return Chapter.published.filter(composition__id=self.kwargs['pk'])


class ChapterView(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    # queryset = Chapter.objects.prefetch_related('pages')
    queryset = (Chapter.objects.all().select_related('composition').
                prefetch_related('pages').
                only('id', 'composition__id','is_published', 'number', 'name', 'upload_date', 'pub_date',))
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if serializer.data.get('is_published'):
            return Response(serializer.data)
        if (not serializer.data.get('is_published')
                and (request.user.is_superuser or instance.composition.publishers.filter(id=request.user.id).exists())):
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChapterDetailSerializer
        return ChapterUpdateSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.AllowAny(), ]
        elif self.action == 'update':
            return [IsOwnerChapter(), ]
        return [permissions.IsAdminUser(), ]


class ChapterCreateView(CreateAPIView):
    """ Создание главы"""
    serializer_class = ChapterCreateSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "composition_id": self.kwargs['composition_id']
            }
        )
        return context

    def perform_create(self, serializer):
        composition = get_object_or_404(Composition, pk=self.kwargs['composition_id'])
        serializer.save(composition=composition)

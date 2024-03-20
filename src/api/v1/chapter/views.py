from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from .models import Chapter
from .serializers import ChapterListSerializer, ChapterDetailSerializer, ChapterCreateSerializer, \
    ChapterUpdateSerializer
from ..composition.models import Composition


class ChapterListView(ListAPIView):
    """ Вывод всех глав произведения"""
    serializer_class = ChapterListSerializer
    queryset = Chapter.objects.all()

    def get_queryset(self):
        return Chapter.objects.filter(composition__id=self.kwargs['pk'])


class ChapterView(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Chapter.objects.prefetch_related('pages')
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChapterDetailSerializer
        return ChapterUpdateSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.AllowAny(), ]
        elif self.action == 'update':
            return [permissions.IsAuthenticated(), ]
        return [permissions.IsAdminUser(), ]


class ChapterCreateView(CreateAPIView):
    """ Создание главы"""
    serializer_class = ChapterCreateSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def perform_create(self, serializer):
        composition = get_object_or_404(Composition, pk=self.kwargs['composition_id'])
        serializer.save(composition=composition)

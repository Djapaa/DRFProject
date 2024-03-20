import django_filters
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, mixins, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from .filters import CatalogSearchFilter
from .models import Composition
from .serializers import CatalogSearchListSerializer, CompositionDetailSerializer, \
    CompositionCreateUpdateSerializer


# Create your views here.

class SearchCatalogView(ListAPIView):
    """ Вывод каталога произведений и поиск по нему"""
    serializer_class = CatalogSearchListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CatalogSearchFilter

    def get_queryset(self):
        return (Composition.objects.all().annotate(avg_rating=Avg('usercompositionrelation__rating'))
                .select_related('type').only('type__name', 'id', 'slug', 'title', 'composition_image'))


class CompositionView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """"""
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get_queryset(self):
        return Composition.objects.all().annotate(
            count_rating=Count('usercompositionrelation__rating', distinct=True),
            avg_rating=Avg('usercompositionrelation__rating'),
            total_in_bookmarks=Count('usercompositionrelation__bookmark', distinct=True)
        ).select_related('status',
                         'age_rating',
                         'type').prefetch_related('genre',
                                                  'author',
                                                  'publishers',
                                                  'tag')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompositionDetailSerializer
        return CompositionCreateUpdateSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]

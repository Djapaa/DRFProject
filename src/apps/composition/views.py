from rest_framework.generics import ListAPIView


from .models import Composition, CompositionsType
from .serializers import CompositionSerializer, CompositionsTypeSerializer


class CompositionView(ListAPIView):
    queryset = Composition.objects.all().select_related('type', 'age_rating', 'status').prefetch_related('tags', 'author', 'genre')
    serializer_class = CompositionSerializer


class TypesView(ListAPIView):
    queryset = CompositionsType.objects.all()
    serializer_class = CompositionsTypeSerializer

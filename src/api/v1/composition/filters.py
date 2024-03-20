import django_filters
from django_filters import FilterSet

from .models import Composition


class CatalogSearchFilter(FilterSet):
    issue_year_gte = django_filters.NumberFilter(field_name="year_of_creations", lookup_expr='gte')
    issue_year_lte = django_filters.NumberFilter(field_name="year_of_creations", lookup_expr='lte')

    class Meta:
        model = Composition
        fields = [
            'type',
            'tag',
            'status',
            'age_rating',
            'genre',
            'issue_year_gte',
            'issue_year_lte',
        ]
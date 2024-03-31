from celery import shared_task
from django.db import transaction
from django.db.models import Count, Avg, Q

from .models import Composition


@shared_task
def calculate_bookmarks_ratings_votes():
    """
    Таска считает и обновляет поля: count_rating, avg_rating, count_bookmarks, total_votes в модели Composition
    """
    compositions = Composition.objects.all().annotate(
        new_total_votes=Count('chapters__votes',
                              filter=Q(chapters__votes__vote__gt=0), distinct=True),
        new_avg_rating=Avg('bookmark_and_rating__rating'),
        new_count_rating=Count('bookmark_and_rating__rating', distinct=True),
        new_count_bookmarks=Count('bookmark_and_rating__bookmark', distinct=True),
    ).prefetch_related('readers', 'author')

    with transaction.atomic():
        for composition in compositions:
            composition.total_votes = composition.new_total_votes
            composition.avg_rating = composition.new_avg_rating or 0
            composition.count_rating = composition.new_count_rating
            composition.count_bookmarks = composition.new_count_bookmarks
            composition.save()

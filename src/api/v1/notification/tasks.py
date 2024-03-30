from celery import shared_task

from ..composition.models import Composition
from .models import UserChapterNotifications


@shared_task
def create_notification_new_chapter_released(composition_id, message):
    composition = Composition.objects.get(id=composition_id)
    for reader in composition.readers.all():
        UserChapterNotifications.objects.create(message=message, user=reader, composition_id=composition_id)

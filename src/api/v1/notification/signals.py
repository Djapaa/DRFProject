from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import create_notification_new_chapter_released
from ..chapter.models import Chapter


@receiver(post_save, sender=Chapter)
def create_notifications(sender, instance, created, **kwargs):
    if created:
        message = f"Глава {instance.number} манги '{instance.composition.title}' была добавлена!"
        create_notification_new_chapter_released.delay(instance.composition.id, message)

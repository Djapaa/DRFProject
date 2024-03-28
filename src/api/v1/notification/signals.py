from django.db.models.signals import post_save
from django.dispatch import receiver

from ..chapter.models import Chapter
from .models import UserChapterNotifications


@receiver(post_save, sender=Chapter)
def create_notifications(sender, instance, created, **kwargs):
    if created:
        message = f"Глава {instance.number} манги '{instance.composition.title}' была добавлена!"
        objs = [
            UserChapterNotifications(
                message=message,
                user=reader,
                composition=instance.composition
            )
            for reader in instance.composition.readers.all()
        ]
        try:
            UserChapterNotifications.objects.bulk_create(objs)
        except:
            print("Ошибка")
from abc import abstractmethod, ABC

from celery import shared_task
from django.core.mail import send_mail

from ..composition.models import Composition
from .models import UserChapterNotifications
from django.conf import settings


class BaseNotificator(ABC):
    @abstractmethod
    def send_notification(self, reader, message, composition):
        pass


class ChapterUpdateWebNotification(BaseNotificator):
    def send_notification(self, reader, message, composition):
        notification = UserChapterNotifications(message=message, user=reader)
        composition.notifications.add(notification, bulk=False)


class ChapterUpdateEmailNotification(BaseNotificator):
    def send_notification(self, reader, message, composition):
        if reader.email_not:
            send_mail(
                "Выход новой главы на 'Абстрактное название сайта'",
                f"{message} Ссылка на главу http://example.com/composition/{composition.slug}",
                settings.EMAIL_HOST_USER,
                [reader.email],
                fail_silently=False,
            )


class Notificator(BaseNotificator):
    def __init__(self, notificators: list[BaseNotificator]):
        self.notificators = notificators

    def send_notification(self, reader, message, composition):
        for notificator in self.notificators:
            notificator.send_notification(reader, message, composition)


@shared_task
def create_notification_new_chapter_released(composition_id, message):
    notificator = Notificator(
        [ChapterUpdateWebNotification(), ChapterUpdateEmailNotification()]
    )
    composition = Composition.objects.get(id=composition_id)
    for reader in composition.readers.all():
        notificator.send_notification(reader, message, composition)


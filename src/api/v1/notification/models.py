from django.contrib.auth import get_user_model
from django.db import models

from ..composition.models import Composition

User = get_user_model()



class UserChapterNotifications(models.Model):
    """
    Модель для уведомления пользователей о выходе новых глав
    """
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chapter_notification')
    message = models.CharField('Текст сообщения', max_length=250)
    created = models.DateTimeField(auto_now=True)
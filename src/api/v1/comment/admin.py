from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Comment


@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    pass
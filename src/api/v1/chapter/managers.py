from django.db import models


class PublishChapterManager(models.Manager):
    """
    Менеджер для филтрации только опубликованных глав
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
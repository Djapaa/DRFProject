from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Comment(MPTTModel):
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    author = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='comments')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    votes = GenericRelation('likedislike.LikeDislike', related_query_name='comment_votes')

    content = models.TextField(verbose_name='Текст комментария', max_length=500)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True,
                            related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('-time_create',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def score(self):
        return self.votes.sum_rating()

    def __str__(self):
        return f'{self.author}:{self.content}'
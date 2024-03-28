from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse



from ..composition.models import Composition

class Chapter(models.Model):
    """ Модель глав произвдеений"""
    name = models.CharField('Название главы', null=True, blank=True)
    number = models.PositiveIntegerField('Номер главы')
    created = models.DateField(auto_now_add=True)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)

    upload_date = models.DateTimeField('Дата загрузки', auto_now_add=True)

    is_published = models.BooleanField(default=False)
    pub_date = models.DateTimeField(null=True, blank=True)

    votes = GenericRelation('likedislike.LikeDislike', related_query_name='chapter')

    class Meta:
        unique_together = ('number', 'composition',)
        ordering = ['number']

    def __str__(self):
        return f"{self.composition.title} Глава {self.number}"

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на статью
        """
        return reverse('chapter', kwargs={'slug': self.composition.slug, 'chapter_number': self.numbers})


class Page(models.Model):
    """ Модель страниц глав"""
    number = models.PositiveIntegerField('Номер страницы')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
    image_page = models.ImageField('Изображение страницы', upload_to='images/chapter_page/')

    class Meta:
        unique_together = ('number', 'chapter',)

    def __str__(self):
        return f"Номер страницы: {self.number}, Глава: {self.chapter.number}"

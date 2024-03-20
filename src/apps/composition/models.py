from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

from .services import get_path_upload_title

User = get_user_model()



class Composition(models.Model):
    AGE_RATING = (
        (1, 'Для всех'),
        (2, '16+'),
        (3, '18+'),
    )

    """ Модель произведения(манги, манхвы...)"""
    slug = models.SlugField(max_length=255, blank=True)
    title = models.CharField('Название произведения', max_length=255)
    english_title = models.CharField('Название произведения на английском языке', max_length=255)
    another_name_title = models.CharField('Другие названия', max_length=500)

    year_of_creations = models.PositiveIntegerField('Год выпуска произведения', default=1980)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    owners = models.ManyToManyField(User, blank=True, null=True)

    description = models.TextField('Описание произведения', blank=True)
    composition_image = models.ImageField(upload_to=get_path_upload_title,
                                          default='composition_image/default_composition_image.jpeg')

    type = models.ForeignKey('CompositionsType', on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey('CompositionsStatus', on_delete=models.SET_NULL, null=True)

    age_rating = models.ForeignKey('CompositionsAgeRating', on_delete=models.SET_NULL, null=True, default=3,
                                   blank=True)

    genre = models.ManyToManyField('Genre')
    author = models.ManyToManyField('Author', blank=True)
    view = models.PositiveIntegerField(default=0) # ЗАТЫЧКА ПОД ПРОСМОТРЫ СТРАНИЦЫ, ПЕРЕДЕЛАТЬ ПОД УНИКАЛЬНЫЕ ПРОСМОТРЫ ПРИ ПОМОЩИ IP USER'A

    # readers = models.ManyToManyField(User, through='UserCompositionRelation', related_name='ratings_and_bookmarks') # Связь для рейтинга и закладок к Произведению

    # comments = GenericRelation('Comment', related_name='comments')

    tags = TaggableManager()


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.english_title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на статью
        """
        return reverse('composition_detail', kwargs={'slug': self.slug})

    def get_genres(self):
        return "\n".join([item.name for item in self.genre.all()])

    def get_authors(self):
        return "\n".join([item.name for item in self.author.all()])

class CompositionsStatus(models.Model):
    """ Модель статуса произведения(Продолжэается, закончен ...)"""
    name = models.CharField('Название статуса', max_length=20)

    def __str__(self):
        return self.name


class CompositionsType(models.Model):
    """ Модель типа произведения (манга, манхва, рукомикс...)"""
    name = models.CharField('Название типа', max_length=20)

    def __str__(self):
        return self.name

class Author(models.Model):
    """ Модель авторов произвдеений"""
    name = models.CharField('Имя автора', max_length=100)

    def __str__(self):
        return self.name

class Genre(models.Model):
    """ Модель жанров произведений"""
    name = models.CharField('Название жанра', max_length=50)

    def __str__(self):
        return self.name


class CompositionsAgeRating(models.Model):
    """ Модель Возрастного рейтинга произведения (16+, 18+, Null)"""
    name = models.CharField('Название возростного рейтинга', max_length=20, default=None, null=True)

    def __str__(self):
        return self.name

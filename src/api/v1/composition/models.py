from django.db import models

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

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

    publishers = models.ManyToManyField(User, blank=True)

    description = models.TextField('Описание произведения', blank=True)
    composition_image = models.ImageField(upload_to=get_path_upload_title,
                                          default='composition_image/default_composition_image.jpeg')

    type = models.ForeignKey('CompositionsType', on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey('CompositionsStatus', on_delete=models.SET_NULL, null=True)

    age_rating = models.ForeignKey('CompositionsAgeRating', on_delete=models.SET_NULL, null=True, default=3,
                                   blank=True)

    tag = models.ManyToManyField('Tag')
    genre = models.ManyToManyField('Genre')
    author = models.ManyToManyField('Author', blank=True)
    view = models.PositiveIntegerField(default=0) # ЗАТЫЧКА ПОД ПРОСМОТРЫ СТРАНИЦЫ, ПЕРЕДЕЛАТЬ ПОД УНИКАЛЬНЫЕ ПРОСМОТРЫ ПРИ ПОМОЩИ IP USER'A

    readers = models.ManyToManyField(User, through='UserCompositionRelation', related_name='ratings_and_bookmarks') # Связь для рейтинга и закладок к Произведению

    # comments = GenericRelation('Comment', related_name='comments')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.english_title)
        super().save(*args, **kwargs)


    def get_avg_rating(self):
        return UserCompositionRelation.objects.filter(composition=self).aggregate(avg_rating=Avg('rating'))['avg_rating']



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

class Tag(models.Model):
    """ Модель жанров произведений"""
    name = models.CharField('Название Тега', max_length=50)

    def __str__(self):
        return self.name


class CompositionsAgeRating(models.Model):
    """ Модель Возрастного рейтинга произведения (16+, 18+, Null)"""
    name = models.CharField('Название возростного рейтинга', max_length=20, default=None, null=True)

    def __str__(self):
        return self.name


class UserCompositionRelation(models.Model):
    class Bookmark(models.IntegerChoices):
        READING = 1, "Читаю"
        WILL_READ = 2, "Буду читать"
        READED = 3, "Прочитано"
        ABANDONED = 4, "Брошено"
        POSTPONED = 5, "Отложенно"

    class Rating(models.IntegerChoices):
        TEN = 10, "Шедевр"
        NINE = 9, "Отлично"
        EIGHT = 8, "Очень хорошо"
        SEVEN = 7, "Хорошо"
        SIX = 6, "Нормально"
        FIVE = 5, "Сомнительно, но окей"
        FOUR = 4, "Ну такое"
        THREE = 3, "Плохо"
        TWO = 2, "Очень плохо"
        ONE = 1, "Крайне плохо"


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark_and_rating')
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, related_name='bookmark_and_rating')
    bookmark = models.PositiveSmallIntegerField(choices=Bookmark.choices, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=Rating.choices, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'composition',)

    def __str__(self):
        return f"user:{self.user}; Comp: {self.composition}; {self.bookmark}, {self.rating}"


    def get_current_bookmark_text(self):
        try:
            return self.Bookmark.choices[self.bookmark - 1][1]
        except:
            return 'Добавить в закладки'

    def __str__(self):
        return f"user:{self.user}; Comp: {self.composition}; {self.bookmark}, {self.rating}"

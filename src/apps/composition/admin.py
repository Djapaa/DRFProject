from django.contrib import admin

from .models import Composition, Genre, Author, CompositionsStatus, \
    CompositionsType, CompositionsAgeRating


@admin.register(CompositionsType)
class CompositionsTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CompositionsStatus)
class CompositionsStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(CompositionsAgeRating)
class CompositionsStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'year_of_creations', 'created', 'updated', 'type', 'status', 'age_rating',
                    'get_genres', 'get_authors', 'tag_list']
    prepopulated_fields = {'slug': ('english_title',)}


    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())







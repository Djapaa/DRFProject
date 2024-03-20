from django.contrib import admin

from .models import Page, Chapter


class ChapterPageInline(admin.StackedInline):
    model = Page


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    inlines = [ChapterPageInline]


@admin.register(Page)
class ChapterPageAdmin(admin.ModelAdmin):
    pass

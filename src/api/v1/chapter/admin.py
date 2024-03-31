from django.contrib import admin

from .models import Page, Chapter


class ChapterPageInline(admin.StackedInline):
    model = Page

@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    for item in queryset:
        item.is_published = True
        item.save()

@admin.action(description="Mark selected stories as unpublished")
def make_unpublished(modeladmin, request, queryset):
    for item in queryset:
        item.is_published = False
        item.save()


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    inlines = [ChapterPageInline]
    actions = [make_published, make_unpublished]


@admin.register(Page)
class ChapterPageAdmin(admin.ModelAdmin):
    pass

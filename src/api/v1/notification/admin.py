from django.contrib import admin

from .models import UserChapterNotifications


@admin.register(UserChapterNotifications)
class UserChapterNotifications(admin.ModelAdmin):
    pass

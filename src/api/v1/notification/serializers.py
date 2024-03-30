from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserChapterNotifications

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    composition_image = serializers.ImageField(source='composition.composition_image', read_only=True)
    slug = serializers.CharField(source='composition.slug', read_only=True)
    message = serializers.CharField(read_only=True)
    composition_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserChapterNotifications
        fields = ('id', 'composition_id', 'message', 'composition_image', 'slug')

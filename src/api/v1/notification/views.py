from rest_framework import mixins, viewsets, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .serializers import NotificationSerializer
from .models import UserChapterNotifications


class NotificationView(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return UserChapterNotifications.objects.filter(user=self.request.user).select_related('user').prefetch_related(
            'composition')

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        notification = get_object_or_404(UserChapterNotifications, pk=serializer.validated_data.get('id'))
        self.perform_destroy(notification)
        return Response(status=status.HTTP_204_NO_CONTENT)

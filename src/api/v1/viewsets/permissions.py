from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Автор комментария или администратор"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff


class IsOwnerChapter(IsOwner):
    def has_object_permission(self, request, view, obj):
        return obj.composition.publishers.filter(id=request.user.id).exists() or request.user.is_staff
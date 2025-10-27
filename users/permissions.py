from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(
            request.user, "is_moderator", False
        )


class IsNotModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and not getattr(
            request.user, "is_moderator", False
        )

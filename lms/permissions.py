from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Проверяет, принадлежит ли пользователь к группе 'Модератор'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
               request.user.groups.filter(name='Модератор').exists()


class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not (request.user and request.user.groups.filter(name='Модератор').exists())
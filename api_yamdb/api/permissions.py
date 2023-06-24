from rest_framework.permissions import BasePermission, SAFE_METHODS

from reviews.models import User


class YamDBPermission(BasePermission):
    """Пермишен для реализации повторяющейся логики"""
    message = 'Доступ запрещен'


class IsAdminOrSuperUserDjango(YamDBPermission):
    """Права для Администратора и Суперпользователя Django."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_staff
                or request.user.role == User.UsersRole.ADMIN
                or request.user.is_superuser
            ))


class IsAdminModeratorOwnerOrReadOnly(YamDBPermission):
    """Права для админа, модератора, хозяина объекта или для чтения."""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == User.UsersRole.ADMIN
                or request.user.role == User.UsersRole.MODERATOR
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(YamDBPermission):
    """Права для Администратора и Суперпользователя Django"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.UsersRole.ADMIN
        )


class IsReadOnly(YamDBPermission):
    """Только для чтения."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

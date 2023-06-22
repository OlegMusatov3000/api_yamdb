from rest_framework.permissions import BasePermission, SAFE_METHODS

from reviews.models import User


MESSAGE = 'Доступ запрещен'


class IsAdminOrSuperUserDjango(BasePermission):
    """Права для Администратора и Суперпользователя Django"""
    message = MESSAGE

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_staff
                or request.user.role == User.UsersRole.ADMIN
                or request.user.is_superuser
            ))


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    message = MESSAGE

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == User.UsersRole.ADMIN
                or request.user.role == User.UsersRole.MODERATOR
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(BasePermission):
    """Права для Администратора и Суперпользователя Django"""
    message = MESSAGE

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.UsersRole.ADMIN
        )


class IsReadOnly(BasePermission):
    message = MESSAGE

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

MESSAGE = 'Доступ запрещен'


class IsAdminOrSuperUserDjango(BasePermission):
    """Права для Администратора и Суперпользователя Django"""
    message = MESSAGE

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_staff
                or request.user.role == 'admin'
            ))


class IsSuperUserOrAdminOrModeratorOrAuthorOrReadOnly(BasePermission):
    message = MESSAGE

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.is_stuff
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user == obj.author
            ))


# Решил не менять чужой пермишн, а сделать свой, на всякий случай
# но они, по идее, должны делать одно и тоже, так что нужно один удалить
class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

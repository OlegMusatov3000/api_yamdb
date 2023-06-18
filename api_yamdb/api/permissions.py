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


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

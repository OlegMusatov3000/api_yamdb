from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    message = (
        "The method is not safe or the user is not the author of the object"
    )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )

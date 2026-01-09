from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Кастомные права доступа.

    Анонимному пользователю предоставляется только право на чтение.
    Аутентифицированный пользователь может создавать записи.
    Изменять, удалять записи может только автор записи.
    """

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return obj.author == request.user
        return request.method in permissions.SAFE_METHODS

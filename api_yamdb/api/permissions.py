from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (request.user in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAmdinOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user in SAFE_METHODS
            or request.user.is_staff or request.user.role == 'admin'
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

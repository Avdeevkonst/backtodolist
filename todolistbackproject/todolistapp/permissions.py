from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True if request.method in permissions.SAFE_METHODS\
                       or obj.owner == request.user or request.user.is_superuser else False



from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow owners of the order to modify it, otherwise read-only
        return obj.customer.user == request.user and not request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create an item.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access for any request
        else:
            return request.user.is_staff  # Only allow POST (create) if user is admin

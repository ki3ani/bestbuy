from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow owners of the order to modify it, otherwise read-only
        return obj.customer.user == request.user and not request.user.is_staff

from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Only staff users have access via "unsafe" methods. All others may
    access as read-only.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only the model instance owner/creator may access via "unsafe"
    methods. All others may access as read-only.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user

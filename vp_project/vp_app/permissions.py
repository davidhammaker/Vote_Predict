from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Only staff users have access via "unsafe" methods. All others may
    access as read-only.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_staff:
            return True
        return False

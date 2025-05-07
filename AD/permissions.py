from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to allow access only to admins.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Only admins can access

class IsPersonnel(BasePermission):
    """
    Custom permission to allow access only to personnel.
    """
    def has_permission(self, request, view):
        return request.user and not request.user.is_staff 
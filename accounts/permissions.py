from rest_framework import permissions


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'instructor'
        return False 
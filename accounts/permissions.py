from rest_framework import permissions


# Custom permission to allow access only to students.
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return True if the requesting user is a student.
        """
        if request.user.is_authenticated:
            return request.user.role == "student"
        return False


# Custom permission to allow access only to instructors.
class IsInstructor(permissions.BasePermission):
    """
    Return True if the requesting user is an instructor.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "instructor"
        return False


#  Custom permission to allow access only to admin users.
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return True if the requesting user is an admin.
        """
        if request.user.is_authenticated:
            return request.user.role == "admin"
        return False

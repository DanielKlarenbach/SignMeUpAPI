
from rest_framework import permissions

from api.models import User, Department


class IsUniversityAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if str(request.user.groups) == 'university_admin':
            return True
        return False

class IsDepartmentAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if str(request.user.groups) == 'department_admin':
            return True
        return False

class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        if str(request.user.groups) == 'student':
            return True
        return False

class IsFromThisUniversity(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.university_id == obj.id:
            return True
        return False

class IsFromThisDepartment(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.department_id == obj.id:
            return True
        return False

class IsAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.id==obj.id:
            return True
        return False

class AllowNoOne(permissions.BasePermission):

    def has_permission(self, request, view):
        return False
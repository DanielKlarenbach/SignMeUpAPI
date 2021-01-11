
from rest_framework import permissions

from api.models import User

class IsDeansOfficeUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if str(request.user.groups) == 'deans_office':
            return True
        return False

class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if str(request.user.groups) == 'admin':
            return True
        return False

class HasPKAsObjectsFK(permissions.BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(pk=view.kwargs['pk'])
        if request.user == user:
            return True
        return False
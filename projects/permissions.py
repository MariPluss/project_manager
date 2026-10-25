
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAdministratorOrManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ['admin', 'manager']
        )


class IsAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.method in SAFE_METHODS
        )


class IsProjectRolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == 'admin':
            return True

        if request.method in SAFE_METHODS:
            return True

        if user.role == 'manager':
            return (
                view.__class__.__name__ in [
                    'TaskListAPIView',
                    'TaskDetailAPIView',
                ]
                and request.method in ['POST', 'PUT', 'PATCH']
            )

        if user.role == 'user':
            return (
                view.__class__.__name__ == 'TaskDetailAPIView'
                and request.method == 'PATCH'
            )

        return False

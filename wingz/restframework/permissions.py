from rest_framework.permissions import BasePermission

from wingz_sso.constants import UserRole


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == UserRole.ADMIN)

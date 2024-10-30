from rest_framework.permissions import IsAuthenticated

from wingz_sso.constants import UserRole


class IsAdminUser(IsAuthenticated):

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.role == UserRole.ADMIN
        )

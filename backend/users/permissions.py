from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class AllowAnyAndIsAuthenticatedForMe(permissions.BasePermission):
    """Предоставит доступ всем к user и аутентифицированным к me."""

    def has_permission(self, request, view):
        if request.path == '/api/users/me/':
            if request.method == "GET":
                return request.user.is_authenticated
            else:
                raise MethodNotAllowed(method=request.method)
        return True

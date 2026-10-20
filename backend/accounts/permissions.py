from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    roles = ()

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in self.roles)

class IsAdmin(HasRole):
    roles = ("admin",)

class IsDoctor(HasRole):
    roles = ("doctor",)

class IsPatient(HasRole):
    roles = ("patient",)

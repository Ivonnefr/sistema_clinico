from rest_framework.permissions import BasePermission
# Solo para clases de permisos

class IsOdontologo(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "odontologo")
    # Si es odontologo se le permite acceder a las vistas protegidas por este permiso, de lo contrario se le deniega el acceso.

class IsRecepcionista(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "recepcionista")
    # Si es recepcionista se le permite acceder a las vistas protegidas por este permiso, de lo contrario se le deniega el acceso.

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request.user, "odontologo") or
            hasattr(request.user, "recepcionista")
        )

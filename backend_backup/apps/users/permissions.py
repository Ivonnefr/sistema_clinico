from rest_framework.permissions import BasePermission
# Solo para clases de permisos

class IsDentist(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "dentist")
    # Si es dentista se le permite acceder a las vistas protegidas por este permiso, de lo contrario se le deniega el acceso.

class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "receptionist")
    # Si es recepcionista se le permite acceder a las vistas protegidas por este permiso, de lo contrario se le deniega el acceso.

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request.user, "dentist") or
            hasattr(request.user, "receptionist")
        )
    
    
class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
from apps.users.permissions import IsActiveUser, IsRecepcionista, IsOdontologo


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_permissions(self):

        # Ver citas
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsActiveUser]

        # Crear cita (solo recepcionista)
        elif self.action == "create":
            permission_classes = [IsActiveUser, IsRecepcionista]

        # Actualizar
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsActiveUser]

        # Eliminar
        elif self.action == "destroy":
            permission_classes = [IsActiveUser, IsRecepcionista]

        else:
            permission_classes = [IsActiveUser]

        return [permission() for permission in permission_classes]